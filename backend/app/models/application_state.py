import uuid

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ApplicationState(Base):
    __tablename__ = "application_states"
    __table_args__ = (
        UniqueConstraint("machine_id", "app_slug", name="uq_application_states_machine_app"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    machine_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("machines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    app_slug: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    app_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    present: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    transition: Mapped[str] = mapped_column(String(50), nullable=False, default="idle", index=True)

    last_operation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    last_job_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    installed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
