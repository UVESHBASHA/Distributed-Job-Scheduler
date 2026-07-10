from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.job import JobCreate
from app.services.job_service import (
    create_new_job,
    list_jobs,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return create_new_job(db, job)


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db),
):
    return list_jobs(db)
