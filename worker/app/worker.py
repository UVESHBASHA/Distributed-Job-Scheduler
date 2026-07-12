import socket

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import SessionLocal


def register_worker():
    db = None
    try:
        db = SessionLocal()

        hostname = socket.gethostname()

        query = text("""
            INSERT INTO workers(name, hostname, status)
            VALUES (:name, :hostname, 'ACTIVE')
            RETURNING id;
        """)

        worker_id = db.execute(
            query,
            {
                "name": settings.WORKER_NAME,
                "hostname": hostname,
            },
        ).scalar()

        db.commit()

        print(f"✅ Worker Registered (ID={worker_id})")

        return worker_id
    except SQLAlchemyError as exc:
        if db is not None:
            db.rollback()
        raise RuntimeError(f"Database connection failed: {exc}") from exc
    finally:
        if db is not None:
            db.close()
