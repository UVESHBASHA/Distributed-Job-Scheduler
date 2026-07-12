"""restore dead letter jobs

Revision ID: 5ad0d43cad9c
Revises: b123456789ab
Create Date: 2026-07-12 18:15:12.715230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ad0d43cad9c'
down_revision: Union[str, Sequence[str], None] = 'b123456789ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
