from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import traceback

from app.database.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        created = register_user(db, user)

        return {
            "message": "User registered successfully",
            "user_id": created.id,
        }

    except Exception as e:
        traceback.print_exc()   # <-- prints the full error in the terminal
        return {
            "error": str(e)
        }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        return login_user(
            db,
            user.email,
            user.password,
        )
    except Exception as e:
        traceback.print_exc()
        return {
            "error": str(e)
        }
