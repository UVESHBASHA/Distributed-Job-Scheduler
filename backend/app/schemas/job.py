from datetime import datetime
from typing import Any

from pydantic import BaseModel


class JobCreate(BaseModel):

    queue_id: int

    name: str

    job_type: str = "IMMEDIATE"

    payload: dict[str, Any] | None = None

    priority: int = 1

    run_at: datetime | None = None

    cron_expression: str | None = None

    max_retries: int = 3


class JobResponse(BaseModel):

    id: int

    queue_id: int

    name: str

    job_type: str

    status: str

    priority: int

    retry_count: int

    max_retries: int

    model_config = {
        "from_attributes": True
    }
