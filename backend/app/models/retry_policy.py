from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class RetryPolicy(Base):
    __tablename__ = "retry_policies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    strategy = Column(String(30), nullable=False)

    max_retries = Column(Integer, default=3)

    initial_delay = Column(Integer, default=5)

    max_delay = Column(Integer, default=300)

    backoff_multiplier = Column(Integer, default=2)

    queues = relationship("Queue", back_populates="retry_policy")
