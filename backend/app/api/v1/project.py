from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.project import ProjectCreate
from app.services.project_service import (
    create_new_project,
    list_projects,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("/")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
):
    return create_new_project(db, project)


@router.get("/")
def get_projects(
    db: Session = Depends(get_db),
):
    return list_projects(db)
