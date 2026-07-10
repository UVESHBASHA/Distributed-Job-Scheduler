from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.organization import OrganizationCreate
from app.services.organization_service import (
    create_new_organization,
    list_organizations,
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post("/")
def create_org(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
):
    # Temporary owner_id until JWT authentication is connected
    owner_id = 1

    return create_new_organization(
        db,
        owner_id,
        organization,
    )


@router.get("/")
def get_all_orgs(
    db: Session = Depends(get_db),
):
    return list_organizations(db)
