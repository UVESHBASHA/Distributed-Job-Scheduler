from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import traceback

from app.database.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
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

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        result = login_user(
            db,
            user.email,
            user.password,
        )

        if not result or result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return result

    except HTTPException:
        raise

    except Exception:
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
