"""forum v2 features

Revision ID: 20260503_forum_v2_features
Revises: 20260503_add_forum_tables
Create Date: 2026-05-03 13:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260503_forum_v2_features"
down_revision: Union[str, Sequence[str], None] = "20260503_add_forum_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "forum_topics",
        sa.Column("views_count", sa.Integer(), nullable=False, server_default="0"),
    )

    op.add_column(
        "forum_posts",
        sa.Column("useful_votes_count", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "forum_post_votes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["post_id"], ["forum_posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("post_id", "user_id", name="uq_forum_post_votes_post_user"),
    )
    op.create_index(op.f("ix_forum_post_votes_post_id"), "forum_post_votes", ["post_id"], unique=False)
    op.create_index(op.f("ix_forum_post_votes_user_id"), "forum_post_votes", ["user_id"], unique=False)

    op.create_table(
        "forum_post_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reporter_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.String(length=100), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["post_id"], ["forum_posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forum_post_reports_post_id"), "forum_post_reports", ["post_id"], unique=False)
    op.create_index(op.f("ix_forum_post_reports_reporter_id"), "forum_post_reports", ["reporter_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_forum_post_reports_reporter_id"), table_name="forum_post_reports")
    op.drop_index(op.f("ix_forum_post_reports_post_id"), table_name="forum_post_reports")
    op.drop_table("forum_post_reports")

    op.drop_index(op.f("ix_forum_post_votes_user_id"), table_name="forum_post_votes")
    op.drop_index(op.f("ix_forum_post_votes_post_id"), table_name="forum_post_votes")
    op.drop_table("forum_post_votes")

    op.drop_column("forum_posts", "useful_votes_count")
    op.drop_column("forum_topics", "views_count")