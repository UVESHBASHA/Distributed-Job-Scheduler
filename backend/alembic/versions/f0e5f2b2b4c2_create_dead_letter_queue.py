"""Create dead letter queue

Revision ID: f0e5f2b2b4c2
Revises: d7bd408b92f5
Create Date: 2026-07-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f0e5f2b2b4c2"
down_revision: Union[str, Sequence[str], None] = "d7bd408b92f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dead_letter_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "job_id",
            sa.Integer(),
            sa.ForeignKey("jobs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "worker_id",
            sa.Integer(),
            sa.ForeignKey("workers.id", ondelete="SET NULL"),
        ),
        sa.Column(
            "reason",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "failed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("dead_letter_jobs")
