from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    retry_policy_id = Column(
        Integer,
        ForeignKey("retry_policies.id", ondelete="SET NULL"),
        nullable=True,
    )

    name = Column(String(150), nullable=False)

    description = Column(Text)

    priority = Column(Integer, default=1)

    concurrency_limit = Column(Integer, default=1)

    is_paused = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    project = relationship("Project", back_populates="queues")

    retry_policy = relationship("RetryPolicy", back_populates="queues")

    jobs = relationship("Job", back_populates="queue", cascade="all, delete-orphan")
