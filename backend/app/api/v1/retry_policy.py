from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.retry_policy import RetryPolicyCreate
from app.services.retry_policy_service import (
    create_new_retry_policy,
    list_retry_policies,
)

router = APIRouter(
    prefix="/retry-policies",
    tags=["Retry Policies"],
)


@router.post("/")
def create_policy(
    policy: RetryPolicyCreate,
    db: Session = Depends(get_db),
):
    return create_new_retry_policy(db, policy)


@router.get("/")
def get_policies(
    db: Session = Depends(get_db),
):
    return list_retry_policies(db)
