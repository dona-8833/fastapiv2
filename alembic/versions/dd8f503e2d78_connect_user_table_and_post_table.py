"""connect user table and post table

Revision ID: dd8f503e2d78
Revises: d1cadec0039d
Create Date: 2026-10-28 09:55:47.308830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd8f503e2d78'
down_revision: Union[str, Sequence[str], None] = 'd1cadec0039d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("post_user_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_column("posts","owner_id")
    op.drop_constraint("post_user_fk","posts")
    pass
