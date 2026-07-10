from sqlalchemy.orm import Session

from app.models.organization import Organization


def create_organization(db: Session, organization: Organization):
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def get_all_organizations(db: Session):
    return db.query(Organization).all()
