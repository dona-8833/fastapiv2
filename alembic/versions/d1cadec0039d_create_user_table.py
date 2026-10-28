"""create user table

Revision ID: d1cadec0039d
Revises: 4445e14774a0
Create Date: 2026-10-28 09:52:50.447704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1cadec0039d'
down_revision: Union[str, Sequence[str], None] = '4445e14774a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("name",sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
