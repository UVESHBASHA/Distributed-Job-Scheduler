"""Add claimed fields to jobs

Revision ID: d7bd408b92f5
Revises: b859b04a2183
Create Date: 2026-07-10 23:39:02.790967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7bd408b92f5'
down_revision: Union[str, Sequence[str], None] = 'b859b04a2183'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "jobs",
        sa.Column("claimed_by", sa.Integer(), nullable=True),
    )

    op.add_column(
        "jobs",
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_jobs_worker",
        "jobs",
        "workers",
        ["claimed_by"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_jobs_worker", "jobs", type_="foreignkey")
    op.drop_column("jobs", "claimed_at")
    op.drop_column("jobs", "claimed_by")
