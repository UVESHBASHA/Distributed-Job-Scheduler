from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.queue import Queue
from app.schemas.queue import QueueCreate, QueueResponse

router = APIRouter(
    prefix="/queues",
    tags=["Queues"],
)

@router.get("/", response_model=list[QueueResponse])
def get_queues(db: Session = Depends(get_db)):
    return db.query(Queue).all()

@router.post("/", response_model=QueueResponse)
def create_queue(
    queue_data: QueueCreate,
    db: Session = Depends(get_db),
):
    queue = Queue(**queue_data.model_dump())

    db.add(queue)
    db.commit()
    db.refresh(queue)

    return queue

@router.patch("/{queue_id}/pause", response_model=QueueResponse)
def pause_queue(
    queue_id: int,
    db: Session = Depends(get_db),
):
    queue = db.query(Queue).filter(Queue.id == queue_id).first()

    if queue is None:
        raise HTTPException(
            status_code=404,
            detail="Queue not found",
        )

    queue.is_paused = True

    db.commit()
    db.refresh(queue)

    return queue

@router.patch("/{queue_id}/resume", response_model=QueueResponse)
def resume_queue(
    queue_id: int,
    db: Session = Depends(get_db),
):
    queue = db.query(Queue).filter(Queue.id == queue_id).first()

    if queue is None:
        raise HTTPException(
            status_code=404,
            detail="Queue not found",
        )

    queue.is_paused = False

    db.commit()
    db.refresh(queue)

    return queue
