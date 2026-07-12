from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db

router = APIRouter(
    prefix="/executions",
    tags=["Executions"],
)

@router.get("/")
def get_executions(db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT
                je.id,
                je.job_id,
                je.worker_id,
                je.status,
                je.execution_time_ms,
                j.name AS job_name
            FROM job_executions je
            JOIN jobs j ON j.id = je.job_id
            ORDER BY je.id DESC
        """)
    )

    return [dict(row._mapping) for row in result]
