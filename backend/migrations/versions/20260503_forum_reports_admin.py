"""forum reports admin

Revision ID: 20260503_forum_reports_admin
Revises: 20260503_forum_md_revisions
Create Date: 2026-05-03 16:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260503_forum_reports_admin"
down_revision: Union[str, Sequence[str], None] = "20260503_forum_md_revisions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "forum_post_reports",
        sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
    )
    op.add_column(
        "forum_post_reports",
        sa.Column("reviewed_by_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "forum_post_reports",
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index(
        op.f("ix_forum_post_reports_status"),
        "forum_post_reports",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_forum_post_reports_reviewed_by_id"),
        "forum_post_reports",
        ["reviewed_by_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_forum_post_reports_reviewed_by_id_users",
        "forum_post_reports",
        "users",
        ["reviewed_by_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_forum_post_reports_reviewed_by_id_users",
        "forum_post_reports",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_forum_post_reports_reviewed_by_id"), table_name="forum_post_reports")
    op.drop_index(op.f("ix_forum_post_reports_status"), table_name="forum_post_reports")
    op.drop_column("forum_post_reports", "reviewed_at")
    op.drop_column("forum_post_reports", "reviewed_by_id")
    op.drop_column("forum_post_reports", "status")