import time

import psutil
from sqlalchemy import text

from app.database import SessionLocal


def start_heartbeat(worker_id: int, interval: int = 10):
    print("💓 Heartbeat service started...")

    while True:
        db = SessionLocal()

        cpu = int(psutil.cpu_percent())

        memory = int(psutil.virtual_memory().percent)

        db.execute(
            text("""
                UPDATE workers
                SET last_heartbeat = NOW()
                WHERE id = :worker_id
            """),
            {"worker_id": worker_id},
        )

        db.execute(
            text("""
                INSERT INTO worker_heartbeats
                (
                    worker_id,
                    cpu_usage,
                    memory_usage,
                    active_jobs
                )
                VALUES
                (
                    :worker_id,
                    :cpu,
                    :memory,
                    0
                )
            """),
            {
                "worker_id": worker_id,
                "cpu": cpu,
                "memory": memory,
            },
        )

        db.commit()
        db.close()

        print(f"💓 Heartbeat | CPU={cpu}% | RAM={memory}%")

        time.sleep(interval)
