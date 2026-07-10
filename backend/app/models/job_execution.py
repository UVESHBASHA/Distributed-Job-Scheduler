from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text,
)

from sqlalchemy.sql import func

from app.database.database import Base


class JobExecution(Base):

    __tablename__ = "job_executions"

    id = Column(Integer, primary_key=True)

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

    status = Column(
        Text,
        nullable=False,
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    execution_time_ms = Column(Integer)

    error_message = Column(Text)
