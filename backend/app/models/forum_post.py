from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    topic_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("forum_topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    parent_post_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("forum_posts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    is_edited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    useful_votes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

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

    author = relationship("User", lazy="joined")

    topic = relationship(
        "ForumTopic",
        back_populates="posts",
        foreign_keys=[topic_id],
    )

    parent_post = relationship(
        "ForumPost",
        remote_side="ForumPost.id",
        foreign_keys=[parent_post_id],
        back_populates="child_posts",
    )

    child_posts = relationship(
        "ForumPost",
        back_populates="parent_post",
        foreign_keys=[parent_post_id],
    )

    votes = relationship(
        "ForumPostVote",
        back_populates="post",
        cascade="all, delete-orphan",
        foreign_keys="ForumPostVote.post_id",
    )

    reports = relationship(
        "ForumPostReport",
        back_populates="post",
        cascade="all, delete-orphan",
        foreign_keys="ForumPostReport.post_id",
    )

    revisions = relationship(
        "ForumPostRevision",
        back_populates="post",
        cascade="all, delete-orphan",
        foreign_keys="ForumPostRevision.post_id",
    )