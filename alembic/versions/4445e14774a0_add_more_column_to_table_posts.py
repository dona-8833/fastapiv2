"""add more column to table posts

Revision ID: 4445e14774a0
Revises: 57766496be2b
Create Date: 2026-10-28 09:47:28.210439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4445e14774a0'
down_revision: Union[str, Sequence[str], None] = '57766496be2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    op.drop_column("posts","created_at")
    pass
