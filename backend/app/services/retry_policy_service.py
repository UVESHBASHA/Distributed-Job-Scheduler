from sqlalchemy.orm import Session

from app.models.retry_policy import RetryPolicy
from app.repositories.retry_policy_repository import (
    create_retry_policy,
    get_retry_policies,
)
from app.schemas.retry_policy import RetryPolicyCreate


def create_new_retry_policy(
    db: Session,
    policy: RetryPolicyCreate,
):

    retry_policy = RetryPolicy(
        name=policy.name,
        strategy=policy.strategy,
        max_retries=policy.max_retries,
        initial_delay=policy.initial_delay,
        max_delay=policy.max_delay,
        backoff_multiplier=policy.backoff_multiplier,
    )

    return create_retry_policy(db, retry_policy)


def list_retry_policies(db: Session):
    return get_retry_policies(db)
