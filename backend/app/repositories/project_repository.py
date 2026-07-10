from sqlalchemy.orm import Session

from app.models.project import Project


def create_project(db: Session, project: Project):
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_projects(db: Session):
    return db.query(Project).all()
