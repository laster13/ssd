from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.forum import ForumAuthorSummary


class ForumNotificationResponse(BaseModel):
    id: UUID
    type: str
    title: str
    message: str | None
    link: str | None
    is_read: bool
    read_at: datetime | None
    created_at: datetime
    actor: ForumAuthorSummary | None

    model_config = ConfigDict(from_attributes=True)


class ForumNotificationCountResponse(BaseModel):
    unread_count: int


class ForumNotificationActionResponse(BaseModel):
    ok: bool
    id: UUID | None = None


class ForumNotificationPreferenceResponse(BaseModel):
    notify_topic_replies: bool
    notify_accepted_answer: bool
    notify_participated_topic_replies: bool

    model_config = ConfigDict(from_attributes=True)


class ForumNotificationPreferenceUpdate(BaseModel):
    notify_topic_replies: bool
    notify_accepted_answer: bool
    notify_participated_topic_replies: bool


class ForumNotificationMarkLinkReadRequest(BaseModel):
    link: str


class ForumUnreadTopicLinksResponse(BaseModel):
    links: list[str]