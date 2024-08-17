"""password reset

Revision ID: 2f5eda52d82d
Revises: 6c8ec07f2dd4
Create Date: 2024-08-15 09:37:22.292538

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2f5eda52d82d"
down_revision: str | None = "6c8ec07f2dd4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "password_resets",
        sa.Column("email", sa.TEXT(), nullable=False),
        sa.Column("token", sa.TEXT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("password_resets")
    # ### end Alembic commands ###