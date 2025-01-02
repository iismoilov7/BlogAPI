"""Create blog table

Revision ID: f986387477d5
Revises: ae74ebe2b6d2
Create Date: 2024-12-23 17:34:55.494836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f986387477d5'
down_revision: Union[str, None] = 'ae74ebe2b6d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("blog", 
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title_ru", sa.String, nullable=False),
        sa.Column("title_en", sa.String, nullable=False),
        sa.Column("content_ru", sa.String, nullable=False),
        sa.Column("content_en", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("category_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.String, nullable=False)
    )
    op.create_foreign_key("blog_user_id_fkey", "blog", "users", ["user_id"], ["user_id"])
    op.create_foreign_key("blog_category_fkey", "blog", "categories", ["category_id"], ["id"])
    

def downgrade() -> None:
    op.drop_constraint("blog_user_id_fkey", "blog", type_="foreignkey")
    op.drop_constraint("blog_category_fkey", "blog", type_="foreignkey")
    op.drop_table("blog")
