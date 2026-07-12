"""restore dead letter jobs"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b123456789ab"
down_revision: Union[str, Sequence[str], None] = "ae3590e65ced"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "dead_letter_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("worker_id", sa.Integer(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column(
            "failed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["jobs.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["worker_id"],
            ["workers.id"],
            ondelete="SET NULL",
        ),
    )

def downgrade() -> None:
    op.drop_table("dead_letter_jobs")
