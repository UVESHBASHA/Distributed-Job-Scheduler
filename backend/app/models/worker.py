from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from app.database.database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    hostname = Column(String(255))

    status = Column(
        String(30),
        default="ACTIVE"
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_heartbeat = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
