import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MachineSettings(Base):
    __tablename__ = "machine_settings"

    machine_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("machines.id", ondelete="CASCADE"),
        primary_key=True,
    )

    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    cloudflare_login: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cloudflare_api_key: Mapped[str | None] = mapped_column(String(255), nullable=True)

    oauth_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    oauth_client: Mapped[str | None] = mapped_column(String(255), nullable=True)
    oauth_secret: Mapped[str | None] = mapped_column(String(255), nullable=True)
    oauth_mail: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    machine = relationship("Machine", back_populates="settings")