from sqlalchemy import text

from app.database import SessionLocal

def claim_next_job(worker_id: int):
    db = SessionLocal()

    try:
        with db.begin():

            # Lock one eligible queue.
            # This prevents multiple workers from racing
            # past the queue concurrency limit.
            queue_result = db.execute(
                text("""
                    SELECT q.id, q.concurrency_limit
                    FROM queues q
                    WHERE q.is_paused = FALSE
                    AND EXISTS (
                        SELECT 1
                        FROM jobs j
                        WHERE j.queue_id = q.id
                        AND j.status = 'QUEUED'
                        AND (
                            j.run_at IS NULL
                            OR j.run_at <= NOW()
                        )
                    )
                    AND (
                        SELECT COUNT(*)
                        FROM jobs running_job
                        WHERE running_job.queue_id = q.id
                        AND running_job.status IN (
                            'CLAIMED',
                            'RUNNING'
                        )
                    ) < q.concurrency_limit
                    ORDER BY q.priority DESC, q.id
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                """)
            )

            queue = queue_result.mappings().first()

            if queue is None:
                return None

            result = db.execute(
                text("""
                    SELECT *
                    FROM jobs
                    WHERE queue_id = :queue_id
                    AND status = 'QUEUED'
                    AND (
                        run_at IS NULL
                        OR run_at <= NOW()
                    )
                    ORDER BY priority DESC, created_at
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                """),
                {
                    "queue_id": queue["id"]
                },
            )

            job = result.mappings().first()

            if job is None:
                return None

            db.execute(
                text("""
                    UPDATE jobs
                    SET
                        status = 'CLAIMED',
                        claimed_by = :worker_id,
                        claimed_at = NOW(),
                        updated_at = NOW()
                    WHERE id = :id
                """),
                {
                    "id": job["id"],
                    "worker_id": worker_id,
                },
            )

            print(
                f"✅ Worker {worker_id} claimed Job "
                f"{job['id']} | Queue {queue['id']} | "
                f"Limit {queue['concurrency_limit']}"
            )

            return dict(job)

    finally:
        db.close()
