import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StreamFusionAddonConfig(Base):
    __tablename__ = "streamfusion_addon_configs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    addon_token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("streamfusion_addon_tokens.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="internal",
        server_default=text("'internal'"),
    )

    language: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="fr",
        server_default=text("'fr'"),
    )

    quality: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="auto",
        server_default=text("'auto'"),
    )

    max_results: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=20,
        server_default=text("20"),
    )

    catalog_title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="StreamFusion",
        server_default=text("'StreamFusion'"),
    )

    settings_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

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
