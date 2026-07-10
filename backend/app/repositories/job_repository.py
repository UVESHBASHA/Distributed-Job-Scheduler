from sqlalchemy.orm import Session

from app.models.job import Job


def create_job(db: Session, job: Job):

    db.add(job)

    db.commit()

    db.refresh(job)

    return job


def get_jobs(db: Session):

    return db.query(Job).all()
