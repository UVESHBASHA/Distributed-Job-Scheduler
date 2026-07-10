from datetime import datetime

from pydantic import BaseModel


class WorkerCreate(BaseModel):
    name: str
    hostname: str


class WorkerResponse(BaseModel):
    id: int
    name: str
    hostname: str
    status: str
    started_at: datetime
    last_heartbeat: datetime

    model_config = {
        "from_attributes": True
    }


class WorkerHeartbeatCreate(BaseModel):
    worker_id: int
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_jobs: int = 0


class WorkerHeartbeatResponse(BaseModel):
    id: int
    worker_id: int
    heartbeat_time: datetime
    cpu_usage: float
    memory_usage: float
    active_jobs: int

    model_config = {
        "from_attributes": True
    }
