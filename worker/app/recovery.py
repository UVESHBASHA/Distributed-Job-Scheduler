from sqlalchemy import text

from app.database import SessionLocal

def recover_stale_workers(stale_seconds: int = 30):
    db = SessionLocal()

    try:
        with db.begin():
            stale_workers = db.execute(
                text("""
                    SELECT id
                    FROM workers
                    WHERE status = 'ACTIVE'
                    AND last_heartbeat IS NOT NULL
                    AND last_heartbeat <
                        NOW() - (:stale_seconds * INTERVAL '1 second')
                    FOR UPDATE SKIP LOCKED
                """),
                {
                    "stale_seconds": stale_seconds,
                },
            ).mappings().all()

            for worker in stale_workers:
                worker_id = worker["id"]

                result = db.execute(
                    text("""
                        UPDATE jobs
                        SET
                            status = 'QUEUED',
                            claimed_by = NULL,
                            claimed_at = NULL,
                            updated_at = NOW()
                        WHERE claimed_by = :worker_id
                        AND status IN ('CLAIMED', 'RUNNING')
                    """),
                    {
                        "worker_id": worker_id,
                    },
                )

                db.execute(
                    text("""
                        UPDATE workers
                        SET status = 'INACTIVE'
                        WHERE id = :worker_id
                    """),
                    {
                        "worker_id": worker_id,
                    },
                )

                print(
                    f"♻️ Recovered stale Worker {worker_id} | "
                    f"Requeued {result.rowcount} jobs"
                )

    except Exception as error:
        db.rollback()
        print(f"Recovery Error: {error}")

    finally:
        db.close()
