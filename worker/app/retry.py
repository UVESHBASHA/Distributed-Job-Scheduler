from sqlalchemy import text

from app.database import SessionLocal


def retry_job(worker_id: int, job: dict):
    db = SessionLocal()

    try:
        if job["retry_count"] + 1 < job["max_retries"]:
            db.execute(
                text("""
                    UPDATE jobs
                    SET
                        status='QUEUED',
                        retry_count=retry_count+1,
                        run_at = NOW() + interval '30 seconds',
                        updated_at=NOW()
                    WHERE id=:id
                """),
                {
                    "id": job["id"]
                }
            )

            db.commit()

            print(f"🔁 Job {job['id']} queued for retry")
        else:
            db.execute(
                text("""
                    CREATE TABLE IF NOT EXISTS dead_letter_jobs (
                        id SERIAL PRIMARY KEY,
                        job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                        worker_id INTEGER REFERENCES workers(id) ON DELETE SET NULL,
                        reason TEXT NOT NULL,
                        failed_at TIMESTAMPTZ DEFAULT NOW()
                    )
                """)
            )

            db.execute(
                text("""
                    INSERT INTO dead_letter_jobs
                    (
                        job_id,
                        worker_id,
                        reason
                    )
                    VALUES
                    (
                        :job_id,
                        :worker_id,
                        'Maximum retries exceeded'
                    )
                """),
                {
                    "job_id": job["id"],
                    "worker_id": worker_id,
                },
            )

            db.execute(
                text("""
                    UPDATE jobs
                    SET
                        status='DEAD',
                        updated_at=NOW()
                    WHERE id=:id
                """),
                {
                    "id": job["id"]
                }
            )

            db.commit()

            print(f"☠️ Job {job['id']} moved to Dead Letter Queue")

    finally:
        db.close()
