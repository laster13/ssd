"""forum notification preferences

Revision ID: 20260503_forum_notif_prefs
Revises: 20260503_forum_notifs
Create Date: 2026-05-03 19:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260503_forum_notif_prefs"
down_revision: Union[str, Sequence[str], None] = "20260503_forum_notifs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "forum_notification_preferences",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("notify_topic_replies", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("notify_accepted_answer", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("notify_participated_topic_replies", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("forum_notification_preferences")