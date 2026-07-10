from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
)

from sqlalchemy.sql import func

from app.database.database import Base


class WorkerHeartbeat(Base):

    __tablename__ = "worker_heartbeats"

    id = Column(Integer, primary_key=True)

    worker_id = Column(
        Integer,
        ForeignKey("workers.id", ondelete="CASCADE"),
        nullable=False,
    )

    heartbeat_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    cpu_usage = Column(Integer)

    memory_usage = Column(Integer)

    active_jobs = Column(Integer, default=0)
