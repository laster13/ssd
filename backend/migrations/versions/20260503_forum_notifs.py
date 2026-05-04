"""forum notifications

Revision ID: 20260503_forum_notifs
Revises: 20260503_forum_reports_admin
Create Date: 2026-05-03 18:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260503_forum_notifs"
down_revision: Union[str, Sequence[str], None] = "20260503_forum_reports_admin"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "forum_notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("link", sa.String(length=500), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_forum_notifications_user_id"), "forum_notifications", ["user_id"], unique=False)
    op.create_index(op.f("ix_forum_notifications_actor_id"), "forum_notifications", ["actor_id"], unique=False)
    op.create_index(op.f("ix_forum_notifications_type"), "forum_notifications", ["type"], unique=False)
    op.create_index(op.f("ix_forum_notifications_is_read"), "forum_notifications", ["is_read"], unique=False)
    op.create_index(op.f("ix_forum_notifications_created_at"), "forum_notifications", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_forum_notifications_created_at"), table_name="forum_notifications")
    op.drop_index(op.f("ix_forum_notifications_is_read"), table_name="forum_notifications")
    op.drop_index(op.f("ix_forum_notifications_type"), table_name="forum_notifications")
    op.drop_index(op.f("ix_forum_notifications_actor_id"), table_name="forum_notifications")
    op.drop_index(op.f("ix_forum_notifications_user_id"), table_name="forum_notifications")
    op.drop_table("forum_notifications")