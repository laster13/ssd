from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ForumTopic(Base):
    __tablename__ = "forum_topics"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    category_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("forum_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), nullable=False, unique=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    related_tutorial_slug: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)

    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    is_pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    is_edited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    posts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    views_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    accepted_post_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("forum_posts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    category = relationship("ForumCategory", lazy="joined")
    author = relationship("User", lazy="joined")

    posts = relationship(
        "ForumPost",
        back_populates="topic",
        cascade="all, delete-orphan",
        foreign_keys="ForumPost.topic_id",
    )

    accepted_post = relationship(
        "ForumPost",
        foreign_keys=[accepted_post_id],
        post_update=True,
    )

    revisions = relationship(
        "ForumTopicRevision",
        back_populates="topic",
        cascade="all, delete-orphan",
        foreign_keys="ForumTopicRevision.topic_id",
    )

    @staticmethod
    def build_slug(title: str) -> str:
        value = unicodedata.normalize("NFD", title.lower())
        value = value.encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
        return value or "topic"