from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.queue import QueueCreate
from app.services.queue_service import (
    create_new_queue,
    list_queues,
)

router = APIRouter(
    prefix="/queues",
    tags=["Queues"],
)


@router.post("/")
def create_queue(
    queue: QueueCreate,
    db: Session = Depends(get_db),
):
    return create_new_queue(db, queue)


@router.get("/")
def get_queues(
    db: Session = Depends(get_db),
):
    return list_queues(db)
