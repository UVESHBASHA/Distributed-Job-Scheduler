from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class JobExecution(Base):
    __tablename__ = "job_executions"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    worker_id = Column(
        Integer,
        ForeignKey("workers.id", ondelete="SET NULL"),
        nullable=True,
    )

    status = Column(String(30), nullable=False)

    started_at = Column(DateTime(timezone=True))

    completed_at = Column(DateTime(timezone=True))

    execution_time_ms = Column(Integer, default=0)

    error_message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    worker = relationship("Worker", back_populates="job_executions")

    job = relationship("Job")
