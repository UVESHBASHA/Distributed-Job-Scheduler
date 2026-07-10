from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.repositories.organization_repository import (
    create_organization,
    get_all_organizations,
)
from app.schemas.organization import OrganizationCreate


def create_new_organization(
    db: Session,
    owner_id: int,
    organization: OrganizationCreate,
):

    org = Organization(
        name=organization.name,
        description=organization.description,
        owner_id=owner_id,
    )

    return create_organization(db, org)


def list_organizations(db: Session):
    return get_all_organizations(db)
