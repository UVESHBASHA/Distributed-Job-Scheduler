from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project_repository import (
    create_project,
    get_projects,
)
from app.schemas.project import ProjectCreate


def create_new_project(
    db: Session,
    project: ProjectCreate,
):

    new_project = Project(
        organization_id=project.organization_id,
        name=project.name,
        description=project.description,
    )

    return create_project(db, new_project)


def list_projects(db: Session):
    return get_projects(db)
