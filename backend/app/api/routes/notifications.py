from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.forum_notification import ForumNotification
from app.models.user import User
from app.schemas.forum import ForumAuthorSummary
from app.schemas.notification import (
    ForumNotificationActionResponse,
    ForumNotificationCountResponse,
    ForumNotificationMarkLinkReadRequest,
    ForumNotificationPreferenceResponse,
    ForumNotificationPreferenceUpdate,
    ForumNotificationResponse,
    ForumUnreadTopicLinksResponse,
)
from app.services.forum_notifications import get_or_create_forum_notification_preferences

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _serialize_author(user: User | None) -> ForumAuthorSummary | None:
    if user is None:
        return None
    return ForumAuthorSummary(id=user.id, email=user.email)


def _serialize_notification(notification: ForumNotification) -> ForumNotificationResponse:
    return ForumNotificationResponse(
        id=notification.id,
        type=notification.type,
        title=notification.title,
        message=notification.message,
        link=notification.link,
        is_read=notification.is_read,
        read_at=notification.read_at,
        created_at=notification.created_at,
        actor=_serialize_author(notification.actor),
    )


@router.get("", response_model=list[ForumNotificationResponse])
def list_notifications(
    only_unread: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(ForumNotification)
        .options(joinedload(ForumNotification.actor))
        .where(ForumNotification.user_id == current_user.id)
        .order_by(ForumNotification.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    if only_unread:
        stmt = stmt.where(ForumNotification.is_read.is_(False))

    notifications = db.execute(stmt).scalars().all()
    return [_serialize_notification(notification) for notification in notifications]


@router.get("/unread-count", response_model=ForumNotificationCountResponse)
def unread_notification_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(func.count(ForumNotification.id)).where(
        ForumNotification.user_id == current_user.id,
        ForumNotification.is_read.is_(False),
    )
    unread_count = db.execute(stmt).scalar_one()
    return ForumNotificationCountResponse(unread_count=int(unread_count or 0))


@router.get("/unread-topic-links", response_model=ForumUnreadTopicLinksResponse)
def unread_topic_links(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(ForumNotification.link)
        .where(
            ForumNotification.user_id == current_user.id,
            ForumNotification.is_read.is_(False),
            ForumNotification.link.is_not(None),
            ForumNotification.link.like("/forum/%"),
        )
        .distinct()
    )

    links = [link for link in db.execute(stmt).scalars().all() if link]
    return ForumUnreadTopicLinksResponse(links=links)


@router.get("/preferences", response_model=ForumNotificationPreferenceResponse)
def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    preferences = get_or_create_forum_notification_preferences(db, user_id=current_user.id)
    db.commit()

    return ForumNotificationPreferenceResponse(
        notify_topic_replies=preferences.notify_topic_replies,
        notify_accepted_answer=preferences.notify_accepted_answer,
        notify_participated_topic_replies=preferences.notify_participated_topic_replies,
    )


@router.put("/preferences", response_model=ForumNotificationPreferenceResponse)
def update_notification_preferences(
    payload: ForumNotificationPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    preferences = get_or_create_forum_notification_preferences(db, user_id=current_user.id)

    preferences.notify_topic_replies = payload.notify_topic_replies
    preferences.notify_accepted_answer = payload.notify_accepted_answer
    preferences.notify_participated_topic_replies = payload.notify_participated_topic_replies

    db.commit()

    return ForumNotificationPreferenceResponse(
        notify_topic_replies=preferences.notify_topic_replies,
        notify_accepted_answer=preferences.notify_accepted_answer,
        notify_participated_topic_replies=preferences.notify_participated_topic_replies,
    )


@router.post("/mark-link-read", response_model=ForumNotificationActionResponse)
def mark_notifications_for_link_as_read(
    payload: ForumNotificationMarkLinkReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    normalized_link = payload.link.strip()
    if not normalized_link:
        return ForumNotificationActionResponse(ok=False, id=None)

    stmt = select(ForumNotification).where(
        ForumNotification.user_id == current_user.id,
        ForumNotification.link == normalized_link,
        ForumNotification.is_read.is_(False),
    )
    notifications = db.execute(stmt).scalars().all()

    if not notifications:
        return ForumNotificationActionResponse(ok=True, id=None)

    now = datetime.now(timezone.utc)
    for notification in notifications:
        notification.is_read = True
        notification.read_at = now

    db.commit()
    return ForumNotificationActionResponse(ok=True, id=None)


@router.post("/{notification_id}/read", response_model=ForumNotificationActionResponse)
def mark_notification_as_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(ForumNotification)
        .where(
            ForumNotification.id == notification_id,
            ForumNotification.user_id == current_user.id,
        )
        .limit(1)
    )
    notification = db.execute(stmt).scalar_one_or_none()

    if notification is None:
        return ForumNotificationActionResponse(ok=False, id=None)

    if not notification.is_read:
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        db.commit()

    return ForumNotificationActionResponse(ok=True, id=notification.id)


@router.post("/read-all", response_model=ForumNotificationActionResponse)
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(ForumNotification).where(
        ForumNotification.user_id == current_user.id,
        ForumNotification.is_read.is_(False),
    )
    notifications = db.execute(stmt).scalars().all()

    now = datetime.now(timezone.utc)
    for notification in notifications:
        notification.is_read = True
        notification.read_at = now

    db.commit()
    return ForumNotificationActionResponse(ok=True, id=None)