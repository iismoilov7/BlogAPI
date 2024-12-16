"""create users table

Revision ID: 3e89305ba15a
Revises: 
Create Date: 2024-12-07 12:51:12.580672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e89305ba15a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String, nullable=False, unique=True),
        sa.Column('name', sa.String(55), nullable=False),
        sa.Column('username', sa.String(30), unique=True, nullable=False),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False, default='user'),
        sa.Column('picture_url', sa.String(600), nullable=True),
        sa.Column('logins', sa.Integer, default=0),
        sa.Column('last_ip', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('last_activity_at', sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('users')
