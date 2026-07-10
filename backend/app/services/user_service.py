from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
)
from app.schemas.user import UserCreate


def register_user(db: Session, user: UserCreate):

    existing = get_user_by_email(db, user.email)

    if existing:
        raise Exception("Email already exists")

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hash_password(user.password),
    )

    return create_user(db, db_user)
