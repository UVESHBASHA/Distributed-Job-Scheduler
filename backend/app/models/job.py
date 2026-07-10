from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    queue_id = Column(
        Integer,
        ForeignKey("queues.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(150), nullable=False)

    job_type = Column(
        String(30),
        default="IMMEDIATE",
    )

    payload = Column(JSON)

    status = Column(
        String(30),
        default="QUEUED",
    )

    priority = Column(
        Integer,
        default=1,
    )

    run_at = Column(DateTime(timezone=True))

    cron_expression = Column(String(100))

    retry_count = Column(
        Integer,
        default=0,
    )

    max_retries = Column(
        Integer,
        default=3,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    queue = relationship("Queue", back_populates="jobs")
