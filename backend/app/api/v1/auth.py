from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import traceback

from app.database.database import get_db
from app.schemas.user import UserCreate
from app.services.user_service import register_user

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
