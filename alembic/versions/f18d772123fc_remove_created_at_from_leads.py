"""remove created_at from leads

Revision ID: f18d772123fc
Revises: 666f1ed06575
Create Date: 2025-08-27 15:33:44.457024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f18d772123fc'
down_revision: Union[str, Sequence[str], None] = '666f1ed06575'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
