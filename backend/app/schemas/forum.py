from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ForumAuthorSummary(BaseModel):
    id: UUID
    email: str

    model_config = ConfigDict(from_attributes=True)


class ForumCategoryResponse(BaseModel):
    id: UUID
    slug: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ForumPostCreate(BaseModel):
    content: str = Field(min_length=3, max_length=20000)
    parent_post_id: UUID | None = None


class ForumPostUpdate(BaseModel):
    content: str = Field(min_length=3, max_length=20000)


class ForumTopicCreate(BaseModel):
    category_slug: str
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10, max_length=20000)
    related_tutorial_slug: str | None = None


class ForumTopicUpdate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10, max_length=20000)
    related_tutorial_slug: str | None = None


class ForumPostResponse(BaseModel):
    id: UUID
    topic_id: UUID
    author: ForumAuthorSummary
    parent_post_id: UUID | None
    parent_author: ForumAuthorSummary | None = None
    parent_excerpt: str | None = None
    content: str
    is_deleted: bool
    is_edited: bool
    useful_votes_count: int
    created_at: datetime
    updated_at: datetime


class ForumTopicListItem(BaseModel):
    id: UUID
    slug: str
    title: str
    content: str
    related_tutorial_slug: str | None
    is_locked: bool
    is_pinned: bool
    is_edited: bool
    posts_count: int
    views_count: int
    accepted_post_id: UUID | None
    created_at: datetime
    updated_at: datetime
    category: ForumCategoryResponse
    author: ForumAuthorSummary


class ForumTopicResponse(BaseModel):
    id: UUID
    slug: str
    title: str
    content: str
    related_tutorial_slug: str | None
    is_locked: bool
    is_pinned: bool
    is_edited: bool
    posts_count: int
    views_count: int
    accepted_post_id: UUID | None
    created_at: datetime
    updated_at: datetime
    category: ForumCategoryResponse
    author: ForumAuthorSummary
    posts: list[ForumPostResponse]


class ForumTopicModerationResponse(BaseModel):
    ok: bool
    topic_id: UUID
    is_locked: bool | None = None
    is_pinned: bool | None = None
    accepted_post_id: UUID | None = None


class ForumVoteResponse(BaseModel):
    ok: bool
    post_id: UUID
    useful_votes_count: int


class ForumDeleteResponse(BaseModel):
    ok: bool
    id: UUID


class ForumPostReportCreate(BaseModel):
    reason: str = Field(min_length=2, max_length=50)
    details: str | None = Field(default=None, max_length=1000)


class ForumReportResponse(BaseModel):
    ok: bool
    report_id: UUID
    post_id: UUID


class ForumReportPostSummary(BaseModel):
    id: UUID
    topic_id: UUID
    topic_slug: str
    topic_title: str
    post_author: ForumAuthorSummary
    post_content: str
    is_deleted: bool


class ForumPostReportAdminItem(BaseModel):
    id: UUID
    reason: str
    details: str | None
    status: str
    created_at: datetime
    reviewed_at: datetime | None
    reporter: ForumAuthorSummary
    reviewed_by: ForumAuthorSummary | None
    post: ForumReportPostSummary


class ForumReportModerationResponse(BaseModel):
    ok: bool
    report_id: UUID
    status: str


class ForumTopicRevisionResponse(BaseModel):
    id: UUID
    topic_id: UUID
    editor: ForumAuthorSummary
    previous_title: str
    previous_content: str
    created_at: datetime


class ForumPostRevisionResponse(BaseModel):
    id: UUID
    post_id: UUID
    editor: ForumAuthorSummary
    previous_content: str
    created_at: datetime