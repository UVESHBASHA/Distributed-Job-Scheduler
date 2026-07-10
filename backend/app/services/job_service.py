from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.job_repository import (
    create_job,
    get_jobs,
)
from app.schemas.job import JobCreate


def create_new_job(
    db: Session,
    job: JobCreate,
):

    new_job = Job(
        queue_id=job.queue_id,
        name=job.name,
        job_type=job.job_type,
        payload=job.payload,
        priority=job.priority,
        run_at=job.run_at,
        cron_expression=job.cron_expression,
        max_retries=job.max_retries,
    )

    return create_job(db, new_job)


def list_jobs(db: Session):

    return get_jobs(db)
