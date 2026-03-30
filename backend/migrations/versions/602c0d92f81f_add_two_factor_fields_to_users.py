"""add two factor fields to users

Revision ID: 602c0d92f81f
Revises: 0112a8845430
Create Date: 2026-03-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "602c0d92f81f"
down_revision: Union[str, Sequence[str], None] = "0112a8845430"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "two_factor_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "two_factor_secret",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.alter_column("users", "two_factor_enabled", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "two_factor_secret")
    op.drop_column("users", "two_factor_enabled")