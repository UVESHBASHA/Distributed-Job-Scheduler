from sqlalchemy.orm import Session

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
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


def login_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        raise Exception("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise Exception("Invalid email or password")

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
