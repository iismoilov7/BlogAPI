"""Add column preview_url

Revision ID: f57aeb2ce894
Revises: f986387477d5
Create Date: 2024-12-25 01:32:01.204756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f57aeb2ce894'
down_revision: Union[str, None] = 'f986387477d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blog', sa.Column('preview_url', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('blog', 'preview_url')
