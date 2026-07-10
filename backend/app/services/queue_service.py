from sqlalchemy.orm import Session

from app.models.queue import Queue
from app.repositories.queue_repository import (
    create_queue,
    get_queues,
)
from app.schemas.queue import QueueCreate


def create_new_queue(
    db: Session,
    queue: QueueCreate,
):

    new_queue = Queue(
        project_id=queue.project_id,
        retry_policy_id=queue.retry_policy_id,
        name=queue.name,
        description=queue.description,
        priority=queue.priority,
        concurrency_limit=queue.concurrency_limit,
    )

    return create_queue(db, new_queue)


def list_queues(db: Session):
    return get_queues(db)
