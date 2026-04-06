"""create application states table

Revision ID: 4c40fca6f315
Revises: c2e8b10c9a4f
Create Date: 2026-04-06 10:30:00.000000
"""

import json
import uuid

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c40fca6f315"
down_revision: Union[str, Sequence[str], None] = "c2e8b10c9a4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ACTIVE_JOB_STATUSES = {"pending", "claimed", "running"}


def upgrade() -> None:
    op.create_table(
        "application_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("machine_id", sa.UUID(), nullable=False),
        sa.Column("app_slug", sa.String(length=100), nullable=False),
        sa.Column("app_name", sa.String(length=255), nullable=True),
        sa.Column("present", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("transition", sa.String(length=50), nullable=False, server_default=sa.text("'idle'")),
        sa.Column("last_operation", sa.String(length=50), nullable=True),
        sa.Column("last_job_id", sa.UUID(), nullable=True),
        sa.Column("last_job_status", sa.String(length=50), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("installed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["machine_id"], ["machines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("machine_id", "app_slug", name="uq_application_states_machine_app"),
    )

    op.create_index(op.f("ix_application_states_machine_id"), "application_states", ["machine_id"], unique=False)
    op.create_index(op.f("ix_application_states_app_slug"), "application_states", ["app_slug"], unique=False)
    op.create_index(op.f("ix_application_states_present"), "application_states", ["present"], unique=False)
    op.create_index(op.f("ix_application_states_transition"), "application_states", ["transition"], unique=False)

    bind = op.get_bind()

    rows = bind.execute(
        sa.text(
            """
            SELECT
                j.id AS job_id,
                j.machine_id,
                j.type AS job_type,
                j.status,
                j.payload,
                j.error_message,
                j.completed_at,
                j.created_at,
                j.updated_at
            FROM jobs j
            WHERE j.type IN ('install_app', 'uninstall_app')
            ORDER BY
                j.machine_id ASC,
                COALESCE(j.payload ->> 'app_slug', '') ASC,
                j.created_at ASC NULLS LAST,
                j.updated_at ASC NULLS LAST,
                j.id ASC
            """
        )
    ).mappings().all()

    states: dict[tuple[object, str], dict] = {}

    for row in rows:
        payload = row["payload"] or {}
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        app_slug = str((payload.get("app_slug") or "")).strip()
        if not app_slug:
            continue

        app_name = str((payload.get("app_name") or app_slug)).strip() or app_slug
        key = (row["machine_id"], app_slug)

        state = states.get(key)
        if state is None:
            state = {
                "id": uuid.uuid4(),
                "machine_id": row["machine_id"],
                "app_slug": app_slug,
                "app_name": app_name,
                "present": False,
                "transition": "idle",
                "last_operation": None,
                "last_job_id": None,
                "last_job_status": None,
                "last_error": None,
                "installed_at": None,
            }
            states[key] = state
        else:
            state["app_name"] = app_name

        job_type = row["job_type"]
        status = row["status"]

        state["last_operation"] = "install" if job_type == "install_app" else "uninstall"
        state["last_job_id"] = row["job_id"]
        state["last_job_status"] = status
        state["last_error"] = row["error_message"]

        if status in ACTIVE_JOB_STATUSES:
            state["transition"] = "installing" if job_type == "install_app" else "uninstalling"
        else:
            state["transition"] = "idle"

        if job_type == "install_app" and status == "completed":
            state["present"] = True
            state["installed_at"] = row["completed_at"] or row["updated_at"] or row["created_at"]

        if job_type == "uninstall_app" and status == "completed":
            state["present"] = False
            state["installed_at"] = None

    for state in states.values():
        bind.execute(
            sa.text(
                """
                INSERT INTO application_states (
                    id,
                    machine_id,
                    app_slug,
                    app_name,
                    present,
                    transition,
                    last_operation,
                    last_job_id,
                    last_job_status,
                    last_error,
                    installed_at
                ) VALUES (
                    :id,
                    :machine_id,
                    :app_slug,
                    :app_name,
                    :present,
                    :transition,
                    :last_operation,
                    :last_job_id,
                    :last_job_status,
                    :last_error,
                    :installed_at
                )
                """
            ),
            state,
        )


def downgrade() -> None:
    op.drop_index(op.f("ix_application_states_transition"), table_name="application_states")
    op.drop_index(op.f("ix_application_states_present"), table_name="application_states")
    op.drop_index(op.f("ix_application_states_app_slug"), table_name="application_states")
    op.drop_index(op.f("ix_application_states_machine_id"), table_name="application_states")
    op.drop_table("application_states")
