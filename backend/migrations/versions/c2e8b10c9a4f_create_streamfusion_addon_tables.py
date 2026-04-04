"""create streamfusion addon tables

Revision ID: c2e8b10c9a4f
Revises: a8ddebd50292
Create Date: 2026-04-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c2e8b10c9a4f"
down_revision: Union[str, Sequence[str], None] = "a8ddebd50292"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "streamfusion_addon_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_streamfusion_addon_tokens_user_id",
        "streamfusion_addon_tokens",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_streamfusion_addon_tokens_token_hash",
        "streamfusion_addon_tokens",
        ["token_hash"],
        unique=True,
    )

    op.create_table(
        "streamfusion_addon_configs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("addon_token_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False, server_default="internal"),
        sa.Column("language", sa.String(length=16), nullable=False, server_default="fr"),
        sa.Column("quality", sa.String(length=16), nullable=False, server_default="auto"),
        sa.Column("max_results", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("catalog_title", sa.String(length=120), nullable=False, server_default="StreamFusion"),
        sa.Column("settings_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["addon_token_id"],
            ["streamfusion_addon_tokens.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_streamfusion_addon_configs_addon_token_id",
        "streamfusion_addon_configs",
        ["addon_token_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_streamfusion_addon_configs_addon_token_id", table_name="streamfusion_addon_configs")
    op.drop_table("streamfusion_addon_configs")

    op.drop_index("ix_streamfusion_addon_tokens_token_hash", table_name="streamfusion_addon_tokens")
    op.drop_index("ix_streamfusion_addon_tokens_user_id", table_name="streamfusion_addon_tokens")
    op.drop_table("streamfusion_addon_tokens")
