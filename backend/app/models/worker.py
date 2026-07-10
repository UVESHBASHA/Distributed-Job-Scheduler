from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    hostname = Column(String(255), nullable=False)

    status = Column(String(30), default="IDLE")

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    last_heartbeat = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    heartbeats = relationship("WorkerHeartbeat", back_populates="worker", cascade="all, delete-orphan")

    job_executions = relationship("JobExecution", back_populates="worker")
