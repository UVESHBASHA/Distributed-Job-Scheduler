from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class WorkerHeartbeat(Base):
    __tablename__ = "worker_heartbeats"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(
        Integer,
        ForeignKey("workers.id", ondelete="CASCADE"),
        nullable=False,
    )

    heartbeat_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    cpu_usage = Column(Float, default=0.0)

    memory_usage = Column(Float, default=0.0)

    active_jobs = Column(Integer, default=0)

    worker = relationship("Worker", back_populates="heartbeats")
