import time
from datetime import datetime, timezone

from croniter import croniter
from sqlalchemy import text

from app.database import SessionLocal
from app.retry import retry_job


def execute_job(worker_id: int, job: dict):
    """
    Execute one claimed job.
    Supports immediate, scheduled and recurring jobs.
    """

    db = SessionLocal()

    try:
        start = time.time()

        db.execute(
            text("""
                UPDATE jobs
                SET
                    status = 'RUNNING',
                    updated_at = NOW()
                WHERE id = :id
            """),
            {"id": job["id"]},
        )

        db.commit()

        print(
            f"🚀 Executing Job {job['id']} : "
            f"{job['name']}"
        )

        time.sleep(5)

        # Demo failure for retry and DLQ testing
        if "PDF" in job["name"]:
            raise Exception("PDF generation failed")

        execution_time = int(
            (time.time() - start) * 1000
        )

        db.execute(
            text("""
                INSERT INTO job_executions
                (
                    job_id,
                    worker_id,
                    status,
                    execution_time_ms
                )
                VALUES
                (
                    :job_id,
                    :worker_id,
                    'COMPLETED',
                    :execution_time
                )
            """),
            {
                "job_id": job["id"],
                "worker_id": worker_id,
                "execution_time": execution_time,
            },
        )

        job_type = str(
            job["job_type"]
        ).upper()

        if job_type == "RECURRING":
            cron_expression = job["cron_expression"]

            if not cron_expression:
                raise ValueError(
                    "Recurring job requires cron expression"
                )

            now = datetime.now(timezone.utc)

            cron = croniter(
                cron_expression,
                now,
            )

            next_run = cron.get_next(datetime)

            db.execute(
                text("""
                    UPDATE jobs
                    SET
                        status = 'QUEUED',
                        run_at = :next_run,
                        claimed_by = NULL,
                        claimed_at = NULL,
                        retry_count = 0,
                        updated_at = NOW()
                    WHERE id = :id
                """),
                {
                    "id": job["id"],
                    "next_run": next_run,
                },
            )

            print(
                f"🔁 Recurring Job {job['id']} "
                f"scheduled for {next_run}"
            )

        else:
            db.execute(
                text("""
                    UPDATE jobs
                    SET
                        status = 'COMPLETED',
                        updated_at = NOW()
                    WHERE id = :id
                """),
                {"id": job["id"]},
            )

        db.commit()

        print(
            f"✅ Job {job['id']} completed "
            f"in {execution_time} ms"
        )

    except Exception as e:
        db.rollback()

        db.execute(
            text("""
                UPDATE jobs
                SET
                    status = 'FAILED',
                    retry_count = retry_count + 1,
                    updated_at = NOW()
                WHERE id = :id
            """),
            {"id": job["id"]},
        )

        db.execute(
            text("""
                INSERT INTO job_executions
                (
                    job_id,
                    worker_id,
                    status,
                    execution_time_ms
                )
                VALUES
                (
                    :job_id,
                    :worker_id,
                    'FAILED',
                    0
                )
            """),
            {
                "job_id": job["id"],
                "worker_id": worker_id,
            },
        )

        db.commit()

        print(f"❌ Job Failed: {e}")

        retry_job(worker_id, job)

    finally:
        db.close()

