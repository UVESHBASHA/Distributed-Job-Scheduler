from sqlalchemy.orm import Session

from app.models.retry_policy import RetryPolicy


def create_retry_policy(db: Session, policy: RetryPolicy):
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def get_retry_policies(db: Session):
    return db.query(RetryPolicy).all()
