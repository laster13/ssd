"""create security audit logs table

Revision ID: 0936126d19ba
Revises: 602c0d92f81f
Create Date: 2026-04-03 08:28:59.640821
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0936126d19ba"
down_revision: Union[str, Sequence[str], None] = "602c0d92f81f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "security_audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column(
            "severity",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'info'"),
        ),
        sa.Column(
            "success",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("actor_type", sa.String(length=20), nullable=True),
        sa.Column(
            "actor_user_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "actor_machine_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "target_user_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "target_machine_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("ip_address", sa.String(length=128), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["actor_user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["actor_machine_id"],
            ["machines.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["target_user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["target_machine_id"],
            ["machines.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_security_audit_logs_event_type"),
        "security_audit_logs",
        ["event_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_severity"),
        "security_audit_logs",
        ["severity"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_success"),
        "security_audit_logs",
        ["success"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_actor_type"),
        "security_audit_logs",
        ["actor_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_actor_user_id"),
        "security_audit_logs",
        ["actor_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_actor_machine_id"),
        "security_audit_logs",
        ["actor_machine_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_target_user_id"),
        "security_audit_logs",
        ["target_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_target_machine_id"),
        "security_audit_logs",
        ["target_machine_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_ip_address"),
        "security_audit_logs",
        ["ip_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_security_audit_logs_created_at"),
        "security_audit_logs",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_security_audit_logs_created_at"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_ip_address"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_target_machine_id"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_target_user_id"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_actor_machine_id"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_actor_user_id"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_actor_type"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_success"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_severity"),
        table_name="security_audit_logs",
    )
    op.drop_index(
        op.f("ix_security_audit_logs_event_type"),
        table_name="security_audit_logs",
    )
    op.drop_table("security_audit_logs")