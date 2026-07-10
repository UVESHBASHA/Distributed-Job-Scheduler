from pydantic import BaseModel


class QueueCreate(BaseModel):
    project_id: int
    retry_policy_id: int | None = None
    name: str
    description: str | None = None
    priority: int = 1
    concurrency_limit: int = 1


class QueueResponse(BaseModel):
    id: int
    project_id: int
    retry_policy_id: int | None
    name: str
    description: str | None
    priority: int
    concurrency_limit: int
    is_paused: bool

    model_config = {
        "from_attributes": True
    }
