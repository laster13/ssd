from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.forum_notification import ForumNotification
from app.models.forum_notification_preference import ForumNotificationPreference


def get_or_create_forum_notification_preferences(
    db: Session,
    *,
    user_id,
) -> ForumNotificationPreference:
    stmt = (
        select(ForumNotificationPreference)
        .where(ForumNotificationPreference.user_id == user_id)
        .limit(1)
    )
    preferences = db.execute(stmt).scalar_one_or_none()

    if preferences is not None:
        return preferences

    preferences = ForumNotificationPreference(
        user_id=user_id,
        notify_topic_replies=True,
        notify_accepted_answer=True,
        notify_participated_topic_replies=True,
    )
    db.add(preferences)
    db.flush()
    return preferences


def create_forum_notification(
    db: Session,
    *,
    user_id,
    actor_id,
    notification_type: str,
    title: str,
    message: str | None = None,
    link: str | None = None,
) -> ForumNotification | None:
    if actor_id is not None and user_id == actor_id:
        return None

    notification = ForumNotification(
        user_id=user_id,
        actor_id=actor_id,
        type=notification_type,
        title=title,
        message=message,
        link=link,
        is_read=False,
    )
    db.add(notification)
    return notification