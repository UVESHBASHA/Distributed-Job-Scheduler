from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, BatchJobCreate
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


@router.post("/batch")
def create_batch_jobs(
    batch: BatchJobCreate,
    db: Session = Depends(get_db),
):
    created_jobs = []

    for job in batch.jobs:
        created_job = create_new_job(db, job)
        created_jobs.append(created_job)

    return {
        "message": "Batch jobs created successfully",
        "count": len(created_jobs),
        "jobs": created_jobs,
    }


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db),
):
    return list_jobs(db)


@router.patch("/{job_id}/cancel")
def cancel_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.status not in ["QUEUED", "CLAIMED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job in {job.status} state",
        )

    job.status = "CANCELLED"

    db.commit()
    db.refresh(job)

    return {
        "message": "Job cancelled successfully",
        "job_id": job.id,
        "status": job.status,
    }
