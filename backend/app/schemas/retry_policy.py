from pydantic import BaseModel


class RetryPolicyCreate(BaseModel):
    name: str
    strategy: str
    max_retries: int
    initial_delay: int
    max_delay: int
    backoff_multiplier: int


class RetryPolicyResponse(BaseModel):
    id: int
    name: str
    strategy: str
    max_retries: int
    initial_delay: int
    max_delay: int
    backoff_multiplier: int

    model_config = {
        "from_attributes": True
    }
