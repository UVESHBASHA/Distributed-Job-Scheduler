from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.worker import Worker

router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
)


@router.get("/")
def get_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()
