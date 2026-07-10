from sqlalchemy.orm import Session

from app.models.queue import Queue


def create_queue(db: Session, queue: Queue):
    db.add(queue)
    db.commit()
    db.refresh(queue)
    return queue


def get_queues(db: Session):
    return db.query(Queue).all()
