"""add forum tables

Revision ID: 20260503_add_forum_tables
Revises: b8f4a0c7f5b1
Create Date: 2026-05-03 12:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260503_add_forum_tables"
down_revision: Union[str, Sequence[str], None] = "b8f4a0c7f5b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "forum_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forum_categories_slug"), "forum_categories", ["slug"], unique=True)

    op.create_table(
        "forum_topics",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("related_tutorial_slug", sa.String(length=120), nullable=True),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_pinned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("posts_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("accepted_post_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["forum_categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forum_topics_category_id"), "forum_topics", ["category_id"], unique=False)
    op.create_index(op.f("ix_forum_topics_author_id"), "forum_topics", ["author_id"], unique=False)
    op.create_index(op.f("ix_forum_topics_related_tutorial_slug"), "forum_topics", ["related_tutorial_slug"], unique=False)
    op.create_index(op.f("ix_forum_topics_slug"), "forum_topics", ["slug"], unique=True)
    op.create_index(op.f("ix_forum_topics_created_at"), "forum_topics", ["created_at"], unique=False)
    op.create_index(op.f("ix_forum_topics_updated_at"), "forum_topics", ["updated_at"], unique=False)

    op.create_table(
        "forum_posts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["topic_id"], ["forum_topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forum_posts_topic_id"), "forum_posts", ["topic_id"], unique=False)
    op.create_index(op.f("ix_forum_posts_author_id"), "forum_posts", ["author_id"], unique=False)
    op.create_index(op.f("ix_forum_posts_created_at"), "forum_posts", ["created_at"], unique=False)

    op.create_foreign_key(
        "fk_forum_topics_accepted_post_id_forum_posts",
        "forum_topics",
        "forum_posts",
        ["accepted_post_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(op.f("ix_forum_topics_accepted_post_id"), "forum_topics", ["accepted_post_id"], unique=False)

    op.execute(
        """
        INSERT INTO forum_categories (id, slug, name, description)
        VALUES
            (gen_random_uuid(), 'tutoriels', 'Tutoriels', 'Questions liées aux tutoriels et guides'),
            (gen_random_uuid(), 'deploiements', 'Déploiements', 'Questions liées aux installations et déploiements'),
            (gen_random_uuid(), 'catalogue', 'Catalogue', 'Questions sur les applications du catalogue'),
            (gen_random_uuid(), 'bugs', 'Bugs', 'Erreurs, incidents et demandes de correction');
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_forum_topics_accepted_post_id"), table_name="forum_topics")
    op.drop_constraint("fk_forum_topics_accepted_post_id_forum_posts", "forum_topics", type_="foreignkey")

    op.drop_index(op.f("ix_forum_posts_created_at"), table_name="forum_posts")
    op.drop_index(op.f("ix_forum_posts_author_id"), table_name="forum_posts")
    op.drop_index(op.f("ix_forum_posts_topic_id"), table_name="forum_posts")
    op.drop_table("forum_posts")

    op.drop_index(op.f("ix_forum_topics_updated_at"), table_name="forum_topics")
    op.drop_index(op.f("ix_forum_topics_created_at"), table_name="forum_topics")
    op.drop_index(op.f("ix_forum_topics_slug"), table_name="forum_topics")
    op.drop_index(op.f("ix_forum_topics_related_tutorial_slug"), table_name="forum_topics")
    op.drop_index(op.f("ix_forum_topics_author_id"), table_name="forum_topics")
    op.drop_index(op.f("ix_forum_topics_category_id"), table_name="forum_topics")
    op.drop_table("forum_topics")

    op.drop_index(op.f("ix_forum_categories_slug"), table_name="forum_categories")
    op.drop_table("forum_categories")