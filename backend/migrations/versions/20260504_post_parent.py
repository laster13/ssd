"""add parent_post_id to forum posts

Revision ID: 20260504_post_parent
Revises: 20260503_forum_notif_prefs
Create Date: 2026-05-04 12:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260504_post_parent"
down_revision: Union[str, Sequence[str], None] = "20260503_forum_notif_prefs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "forum_posts",
        sa.Column("parent_post_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index(
        op.f("ix_forum_posts_parent_post_id"),
        "forum_posts",
        ["parent_post_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_forum_posts_parent_post_id_forum_posts",
        "forum_posts",
        "forum_posts",
        ["parent_post_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_forum_posts_parent_post_id_forum_posts",
        "forum_posts",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_forum_posts_parent_post_id"), table_name="forum_posts")
    op.drop_column("forum_posts", "parent_post_id")