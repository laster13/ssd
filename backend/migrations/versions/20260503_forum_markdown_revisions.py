"""forum markdown revisions

Revision ID: 20260503_forum_md_revisions
Revises: 20260503_forum_v2_features
Create Date: 2026-05-03 14:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260503_forum_md_revisions"
down_revision: Union[str, Sequence[str], None] = "20260503_forum_v2_features"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "forum_topics",
        sa.Column("is_edited", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "forum_posts",
        sa.Column("is_edited", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    op.create_table(
        "forum_topic_revisions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("editor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("previous_title", sa.Text(), nullable=False),
        sa.Column("previous_content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["topic_id"], ["forum_topics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["editor_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forum_topic_revisions_topic_id"), "forum_topic_revisions", ["topic_id"], unique=False)
    op.create_index(op.f("ix_forum_topic_revisions_editor_id"), "forum_topic_revisions", ["editor_id"], unique=False)
    op.create_index(op.f("ix_forum_topic_revisions_created_at"), "forum_topic_revisions", ["created_at"], unique=False)

    op.create_table(
        "forum_post_revisions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("editor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("previous_content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["post_id"], ["forum_posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["editor_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forum_post_revisions_post_id"), "forum_post_revisions", ["post_id"], unique=False)
    op.create_index(op.f("ix_forum_post_revisions_editor_id"), "forum_post_revisions", ["editor_id"], unique=False)
    op.create_index(op.f("ix_forum_post_revisions_created_at"), "forum_post_revisions", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_forum_post_revisions_created_at"), table_name="forum_post_revisions")
    op.drop_index(op.f("ix_forum_post_revisions_editor_id"), table_name="forum_post_revisions")
    op.drop_index(op.f("ix_forum_post_revisions_post_id"), table_name="forum_post_revisions")
    op.drop_table("forum_post_revisions")

    op.drop_index(op.f("ix_forum_topic_revisions_created_at"), table_name="forum_topic_revisions")
    op.drop_index(op.f("ix_forum_topic_revisions_editor_id"), table_name="forum_topic_revisions")
    op.drop_index(op.f("ix_forum_topic_revisions_topic_id"), table_name="forum_topic_revisions")
    op.drop_table("forum_topic_revisions")

    op.drop_column("forum_posts", "is_edited")
    op.drop_column("forum_topics", "is_edited")