from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db

router = APIRouter(
    prefix="/dead-letter",
    tags=["Dead Letter Queue"],
)

@router.get("/")
def get_dead_letter_jobs(
    db: Session = Depends(get_db),
):
    result = db.execute(
        text("""
            SELECT
                d.id,
                d.job_id,
                d.worker_id,
                d.reason,
                d.failed_at,
                j.name,
                j.status,
                j.retry_count,
                j.max_retries
            FROM dead_letter_jobs d
            JOIN jobs j ON j.id = d.job_id
            ORDER BY d.failed_at DESC
        """)
    )

    return result.mappings().all()

@router.patch("/{job_id}/requeue")
def requeue_dead_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.execute(
        text("""
            SELECT id, status
            FROM jobs
            WHERE id = :job_id
        """),
        {"job_id": job_id},
    ).mappings().first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job["status"] != "DEAD":
        raise HTTPException(
            status_code=400,
            detail="Only DEAD jobs can be requeued",
        )

    db.execute(
        text("""
            UPDATE jobs
            SET
                status = 'QUEUED',
                retry_count = 0,
                claimed_by = NULL,
                claimed_at = NULL,
                updated_at = NOW()
            WHERE id = :job_id
        """),
        {"job_id": job_id},
    )

    db.execute(
        text("""
            DELETE FROM dead_letter_jobs
            WHERE job_id = :job_id
        """),
        {"job_id": job_id},
    )

    db.commit()

    return {
        "message": "Dead job requeued successfully",
        "job_id": job_id,
        "status": "QUEUED",
    }
