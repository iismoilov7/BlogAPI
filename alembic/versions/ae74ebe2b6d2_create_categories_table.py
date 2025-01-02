"""Create category table

Revision ID: ae74ebe2b6d2
Revises: 3e89305ba15a
Create Date: 2024-12-23 14:56:17.747978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae74ebe2b6d2'
down_revision: Union[str, None] = '3e89305ba15a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("categories", 
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name_ru", sa.String, nullable=False, unique=True),
        sa.Column("name_en", sa.String, nullable=False, unique=True),
        sa.Column("articles_length", sa.Integer, nullable=False, default=0),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    

def downgrade() -> None:
    op.drop_table("categories")
