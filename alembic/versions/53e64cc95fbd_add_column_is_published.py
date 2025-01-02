"""Add column is_published

Revision ID: 53e64cc95fbd
Revises: f57aeb2ce894
Create Date: 2024-12-26 00:22:47.648641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53e64cc95fbd'
down_revision: Union[str, None] = 'f57aeb2ce894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("blog", sa.Column("is_published", sa.Boolean, nullable=False, default=False))

def downgrade() -> None:
    op.drop_column("blog", "is_published")
