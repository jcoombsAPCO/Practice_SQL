"""Create Albums Table

Revision ID: 5dad644460f9
Revises: 
Create Date: 2025-05-19 14:36:11.576014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dad644460f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "Albums",
         sa.Column("title", sa.String(50), nullable=False),
         sa.Column("release", sa.Date, nullable=False),
         sa.Column("id", sa.Integer, primary_key=True)
    )


def downgrade() -> None:
    op.drop_table("Albums")
