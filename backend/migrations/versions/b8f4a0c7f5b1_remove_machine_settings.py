"""remove machine settings

Revision ID: b8f4a0c7f5b1
Revises: a8ddebd50292
Create Date: 2026-04-07 11:30:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b8f4a0c7f5b1"
down_revision: Union[str, Sequence[str], None] = "a8ddebd50292"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("machine_settings")


def downgrade() -> None:
    op.create_table(
        "machine_settings",
        sa.Column("machine_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column("cloudflare_login", sa.String(length=255), nullable=True),
        sa.Column("cloudflare_api_key", sa.String(length=255), nullable=True),
        sa.Column("oauth_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("oauth_client", sa.String(length=255), nullable=True),
        sa.Column("oauth_secret", sa.String(length=255), nullable=True),
        sa.Column("oauth_mail", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["machine_id"], ["machines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("machine_id"),
    )
