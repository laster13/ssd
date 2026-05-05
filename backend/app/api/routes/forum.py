import re
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_admin, get_current_user
from app.core.database import get_db
from app.models.forum_category import ForumCategory
from app.models.forum_post import ForumPost
from app.models.forum_post_report import ForumPostReport
from app.models.forum_post_revision import ForumPostRevision
from app.models.forum_post_vote import ForumPostVote
from app.models.forum_topic import ForumTopic
from app.models.forum_topic_revision import ForumTopicRevision
from app.models.user import User
from app.schemas.forum import (
    ForumAuthorSummary,
    ForumCategoryResponse,
    ForumDeleteResponse,
    ForumPostCreate,
    ForumPostReportAdminItem,
    ForumPostReportCreate,
    ForumPostResponse,
    ForumPostRevisionResponse,
    ForumPostUpdate,
    ForumReportModerationResponse,
    ForumReportPostSummary,
    ForumReportResponse,
    ForumTopicCreate,
    ForumTopicListItem,
    ForumTopicModerationResponse,
    ForumTopicResponse,
    ForumTopicRevisionResponse,
    ForumTopicUpdate,
    ForumVoteResponse,
)
from app.services.forum_notifications import (
    create_forum_notification,
    get_or_create_forum_notification_preferences,
)

router = APIRouter(prefix="/forum", tags=["forum"])


def _clean_slug(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip().lower()
    if not value:
        return None
    if not re.fullmatch(r"[a-z0-9-]+", value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug invalide. Utilise uniquement lettres minuscules, chiffres et tirets.",
        )
    return value


def _build_excerpt(value: str | None, max_length: int = 140) -> str | None:
    if value is None:
        return None
    clean = re.sub(r"\s+", " ", value).strip()
    if not clean:
        return None
    if len(clean) <= max_length:
        return clean
    return clean[: max_length - 1].rstrip() + "…"


def _serialize_author(user: User) -> ForumAuthorSummary:
    return ForumAuthorSummary(id=user.id, email=user.email)


def _serialize_post(post: ForumPost) -> ForumPostResponse:
    if post.author is None:
        raise HTTPException(status_code=500, detail="Forum post author missing")

    parent_author = None
    parent_excerpt = None
    if post.parent_post is not None and not post.parent_post.is_deleted:
        if post.parent_post.author is not None:
            parent_author = _serialize_author(post.parent_post.author)
        parent_excerpt = _build_excerpt(post.parent_post.content)

    return ForumPostResponse(
        id=post.id,
        topic_id=post.topic_id,
        author=_serialize_author(post.author),
        parent_post_id=post.parent_post_id,
        parent_author=parent_author,
        parent_excerpt=parent_excerpt,
        content=post.content,
        is_deleted=post.is_deleted,
        is_edited=post.is_edited,
        useful_votes_count=int(post.useful_votes_count or 0),
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def _serialize_topic_list_item(topic: ForumTopic) -> ForumTopicListItem:
    if topic.author is None:
        raise HTTPException(status_code=500, detail="Forum topic author missing")
    if topic.category is None:
        raise HTTPException(status_code=500, detail="Forum topic category missing")

    return ForumTopicListItem(
        id=topic.id,
        slug=topic.slug,
        title=topic.title,
        content=topic.content,
        related_tutorial_slug=topic.related_tutorial_slug,
        is_locked=topic.is_locked,
        is_pinned=topic.is_pinned,
        is_edited=topic.is_edited,
        posts_count=int(topic.posts_count or 0),
        views_count=int(topic.views_count or 0),
        accepted_post_id=topic.accepted_post_id,
        created_at=topic.created_at,
        updated_at=topic.updated_at,
        category=ForumCategoryResponse.model_validate(topic.category),
        author=_serialize_author(topic.author),
    )


def _serialize_topic(topic: ForumTopic) -> ForumTopicResponse:
    if topic.author is None:
        raise HTTPException(status_code=500, detail="Forum topic author missing")
    if topic.category is None:
        raise HTTPException(status_code=500, detail="Forum topic category missing")

    visible_posts = [post for post in topic.posts if not post.is_deleted]

    return ForumTopicResponse(
        id=topic.id,
        slug=topic.slug,
        title=topic.title,
        content=topic.content,
        related_tutorial_slug=topic.related_tutorial_slug,
        is_locked=topic.is_locked,
        is_pinned=topic.is_pinned,
        is_edited=topic.is_edited,
        posts_count=int(topic.posts_count or 0),
        views_count=int(topic.views_count or 0),
        accepted_post_id=topic.accepted_post_id,
        created_at=topic.created_at,
        updated_at=topic.updated_at,
        category=ForumCategoryResponse.model_validate(topic.category),
        author=_serialize_author(topic.author),
        posts=[_serialize_post(post) for post in visible_posts],
    )


def _serialize_report(report: ForumPostReport) -> ForumPostReportAdminItem:
    if report.reporter is None:
        raise HTTPException(status_code=500, detail="Forum report reporter missing")
    if report.post is None:
        raise HTTPException(status_code=500, detail="Forum report post missing")
    if report.post.topic is None:
        raise HTTPException(status_code=500, detail="Forum report topic missing")
    if report.post.author is None:
        raise HTTPException(status_code=500, detail="Forum report post author missing")

    return ForumPostReportAdminItem(
        id=report.id,
        reason=report.reason,
        details=report.details,
        status=report.status,
        created_at=report.created_at,
        reviewed_at=report.reviewed_at,
        reporter=_serialize_author(report.reporter),
        reviewed_by=_serialize_author(report.reviewed_by) if report.reviewed_by else None,
        post=ForumReportPostSummary(
            id=report.post.id,
            topic_id=report.post.topic_id,
            topic_slug=report.post.topic.slug,
            topic_title=report.post.topic.title,
            post_author=_serialize_author(report.post.author),
            post_content=report.post.content,
            is_deleted=report.post.is_deleted,
        ),
    )


def _get_category_by_slug(db: Session, slug: str) -> ForumCategory:
    stmt = select(ForumCategory).where(ForumCategory.slug == slug).limit(1)
    category = db.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return category


def _get_topic_by_slug(db: Session, slug: str) -> ForumTopic:
    stmt = (
        select(ForumTopic)
        .options(
            joinedload(ForumTopic.author),
            joinedload(ForumTopic.category),
            joinedload(ForumTopic.posts).joinedload(ForumPost.author),
            joinedload(ForumTopic.posts).joinedload(ForumPost.parent_post).joinedload(ForumPost.author),
        )
        .where(ForumTopic.slug == slug)
        .limit(1)
    )
    topic = db.execute(stmt).unique().scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=404, detail="Sujet introuvable")
    return topic


def _get_topic_by_id(db: Session, topic_id: UUID) -> ForumTopic:
    stmt = (
        select(ForumTopic)
        .options(
            joinedload(ForumTopic.author),
            joinedload(ForumTopic.category),
        )
        .where(ForumTopic.id == topic_id)
        .limit(1)
    )
    topic = db.execute(stmt).scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=404, detail="Sujet introuvable")
    return topic


def _get_post_by_id(db: Session, post_id: UUID) -> ForumPost:
    stmt = (
        select(ForumPost)
        .options(
            joinedload(ForumPost.author),
            joinedload(ForumPost.parent_post).joinedload(ForumPost.author),
            joinedload(ForumPost.topic).joinedload(ForumTopic.author),
            joinedload(ForumPost.topic).joinedload(ForumTopic.category),
        )
        .where(ForumPost.id == post_id)
        .limit(1)
    )
    post = db.execute(stmt).scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Message introuvable")
    return post


def _get_report_by_id(db: Session, report_id: UUID) -> ForumPostReport:
    stmt = (
        select(ForumPostReport)
        .options(
            joinedload(ForumPostReport.reporter),
            joinedload(ForumPostReport.reviewed_by),
            joinedload(ForumPostReport.post).joinedload(ForumPost.topic),
            joinedload(ForumPostReport.post).joinedload(ForumPost.author),
        )
        .where(ForumPostReport.id == report_id)
        .limit(1)
    )
    report = db.execute(stmt).scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="Signalement introuvable")
    return report


def _build_unique_topic_slug(db: Session, title: str, exclude_topic_id: UUID | None = None) -> str:
    base_slug = ForumTopic.build_slug(title)
    slug = base_slug
    index = 2

    while True:
        stmt = select(ForumTopic.id).where(ForumTopic.slug == slug).limit(1)
        existing_id = db.execute(stmt).scalar_one_or_none()

        if existing_id is None or existing_id == exclude_topic_id:
            return slug

        slug = f"{base_slug}-{index}"
        index += 1


@router.get("/categories", response_model=list[ForumCategoryResponse])
def list_forum_categories(db: Session = Depends(get_db)):
    stmt = select(ForumCategory).order_by(ForumCategory.name.asc())
    categories = db.execute(stmt).scalars().all()
    return [ForumCategoryResponse.model_validate(category) for category in categories]


@router.get("/topics", response_model=list[ForumTopicListItem])
def list_forum_topics(
    category_slug: str | None = Query(default=None),
    related_tutorial_slug: str | None = Query(default=None),
    only_unsolved: bool = Query(default=False),
    q: str | None = Query(default=None),
    sort: str = Query(default="recent"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = (
        select(ForumTopic)
        .options(
            joinedload(ForumTopic.author),
            joinedload(ForumTopic.category),
        )
    )

    cleaned_category_slug = _clean_slug(category_slug)
    cleaned_tutorial_slug = _clean_slug(related_tutorial_slug)

    if cleaned_category_slug:
        stmt = stmt.join(ForumCategory).where(ForumCategory.slug == cleaned_category_slug)

    if cleaned_tutorial_slug:
        stmt = stmt.where(ForumTopic.related_tutorial_slug == cleaned_tutorial_slug)

    if only_unsolved:
        stmt = stmt.where(ForumTopic.accepted_post_id.is_(None))

    if q and q.strip():
        query = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                ForumTopic.title.ilike(query),
                ForumTopic.content.ilike(query),
            )
        )

    if sort == "active":
        stmt = stmt.order_by(
            ForumTopic.is_pinned.desc(),
            ForumTopic.updated_at.desc(),
            ForumTopic.created_at.desc(),
        )
    elif sort == "views":
        stmt = stmt.order_by(
            ForumTopic.is_pinned.desc(),
            ForumTopic.views_count.desc(),
            ForumTopic.updated_at.desc(),
        )
    elif sort == "oldest":
        stmt = stmt.order_by(
            ForumTopic.is_pinned.desc(),
            ForumTopic.created_at.asc(),
        )
    else:
        stmt = stmt.order_by(
            ForumTopic.is_pinned.desc(),
            ForumTopic.created_at.desc(),
        )

    stmt = stmt.offset(offset).limit(limit)

    topics = db.execute(stmt).scalars().all()
    return [_serialize_topic_list_item(topic) for topic in topics]


@router.get("/topics/{topic_slug}", response_model=ForumTopicResponse)
def get_forum_topic(
    topic_slug: str,
    posts_sort: str = Query(default="oldest"),
    db: Session = Depends(get_db),
):
    topic = _get_topic_by_slug(db, topic_slug)
    topic.views_count = int(topic.views_count or 0) + 1
    db.commit()
    db.refresh(topic)

    topic = _get_topic_by_slug(db, topic_slug)

    visible_posts = [post for post in topic.posts if not post.is_deleted]

    if posts_sort == "newest":
        visible_posts.sort(key=lambda post: (post.created_at, post.id), reverse=True)
    elif posts_sort == "useful":
        visible_posts.sort(
            key=lambda post: (
                0 if topic.accepted_post_id == post.id else 1,
                -(int(post.useful_votes_count or 0)),
                post.created_at,
            )
        )
    else:
        visible_posts.sort(key=lambda post: (post.created_at, post.id))

    topic.posts = visible_posts
    return _serialize_topic(topic)


@router.get("/topics/{topic_id}/revisions", response_model=list[ForumTopicRevisionResponse])
def list_forum_topic_revisions(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    stmt = (
        select(ForumTopicRevision)
        .options(joinedload(ForumTopicRevision.editor))
        .where(ForumTopicRevision.topic_id == topic_id)
        .order_by(ForumTopicRevision.created_at.desc())
    )
    rows = db.execute(stmt).scalars().all()

    return [
        ForumTopicRevisionResponse(
            id=row.id,
            topic_id=row.topic_id,
            editor=_serialize_author(row.editor),
            previous_title=row.previous_title,
            previous_content=row.previous_content,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.get("/posts/{post_id}/revisions", response_model=list[ForumPostRevisionResponse])
def list_forum_post_revisions(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    stmt = (
        select(ForumPostRevision)
        .options(joinedload(ForumPostRevision.editor))
        .where(ForumPostRevision.post_id == post_id)
        .order_by(ForumPostRevision.created_at.desc())
    )
    rows = db.execute(stmt).scalars().all()

    return [
        ForumPostRevisionResponse(
            id=row.id,
            post_id=row.post_id,
            editor=_serialize_author(row.editor),
            previous_content=row.previous_content,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.get("/reports", response_model=list[ForumPostReportAdminItem])
def list_forum_reports(
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    stmt = (
        select(ForumPostReport)
        .options(
            joinedload(ForumPostReport.reporter),
            joinedload(ForumPostReport.reviewed_by),
            joinedload(ForumPostReport.post).joinedload(ForumPost.topic),
            joinedload(ForumPostReport.post).joinedload(ForumPost.author),
        )
        .order_by(ForumPostReport.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    if status_filter:
        stmt = stmt.where(ForumPostReport.status == status_filter.strip().lower())

    reports = db.execute(stmt).scalars().all()
    return [_serialize_report(report) for report in reports]


@router.get("/posts/{post_id}/reports", response_model=list[ForumPostReportAdminItem])
def list_reports_for_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    stmt = (
        select(ForumPostReport)
        .options(
            joinedload(ForumPostReport.reporter),
            joinedload(ForumPostReport.reviewed_by),
            joinedload(ForumPostReport.post).joinedload(ForumPost.topic),
            joinedload(ForumPostReport.post).joinedload(ForumPost.author),
        )
        .where(ForumPostReport.post_id == post_id)
        .order_by(ForumPostReport.created_at.desc())
    )

    reports = db.execute(stmt).scalars().all()
    return [_serialize_report(report) for report in reports]


@router.post("/reports/{report_id}/resolve", response_model=ForumReportModerationResponse)
def resolve_forum_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    report = _get_report_by_id(db, report_id)
    report.status = "resolved"
    report.reviewed_by_id = current_user.id
    report.reviewed_at = datetime.now(timezone.utc)
    db.commit()

    return ForumReportModerationResponse(ok=True, report_id=report.id, status=report.status)


@router.post("/reports/{report_id}/dismiss", response_model=ForumReportModerationResponse)
def dismiss_forum_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    report = _get_report_by_id(db, report_id)
    report.status = "dismissed"
    report.reviewed_by_id = current_user.id
    report.reviewed_at = datetime.now(timezone.utc)
    db.commit()

    return ForumReportModerationResponse(ok=True, report_id=report.id, status=report.status)


@router.post("/topics", response_model=ForumTopicResponse, status_code=status.HTTP_201_CREATED)
def create_forum_topic(
    payload: ForumTopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_slug = _clean_slug(payload.category_slug)
    related_tutorial_slug = _clean_slug(payload.related_tutorial_slug)

    if category_slug is None:
        raise HTTPException(status_code=400, detail="category_slug est requis")

    category = _get_category_by_slug(db, category_slug)
    topic_slug = _build_unique_topic_slug(db, payload.title)

    topic = ForumTopic(
        category_id=category.id,
        author_id=current_user.id,
        title=payload.title.strip(),
        slug=topic_slug,
        content=payload.content.strip(),
        related_tutorial_slug=related_tutorial_slug,
        posts_count=0,
        views_count=0,
        is_edited=False,
    )

    db.add(topic)
    db.commit()

    topic = _get_topic_by_slug(db, topic.slug)
    return _serialize_topic(topic)


@router.put("/topics/{topic_id}", response_model=ForumTopicResponse)
def update_forum_topic(
    topic_id: UUID,
    payload: ForumTopicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = _get_topic_by_id(db, topic_id)

    if topic.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    revision = ForumTopicRevision(
        topic_id=topic.id,
        editor_id=current_user.id,
        previous_title=topic.title,
        previous_content=topic.content,
    )
    db.add(revision)

    topic.title = payload.title.strip()
    topic.content = payload.content.strip()
    topic.related_tutorial_slug = _clean_slug(payload.related_tutorial_slug)
    topic.slug = _build_unique_topic_slug(db, topic.title, exclude_topic_id=topic.id)
    topic.is_edited = True

    db.commit()

    topic = _get_topic_by_slug(db, topic.slug)
    return _serialize_topic(topic)


@router.delete("/topics/{topic_id}", response_model=ForumDeleteResponse)
def delete_forum_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = _get_topic_by_id(db, topic_id)

    if topic.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    db.delete(topic)
    db.commit()

    return ForumDeleteResponse(ok=True, id=topic_id)


@router.post("/topics/{topic_id}/posts", response_model=ForumPostResponse, status_code=status.HTTP_201_CREATED)
def create_forum_post(
    topic_id: UUID,
    payload: ForumPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = _get_topic_by_id(db, topic_id)

    if topic.is_locked:
        raise HTTPException(status_code=409, detail="Ce sujet est verrouillé")

    parent_post = None
    if payload.parent_post_id is not None:
        parent_post = _get_post_by_id(db, payload.parent_post_id)

        if parent_post.topic_id != topic.id:
            raise HTTPException(
                status_code=400,
                detail="Le message parent n'appartient pas à ce sujet",
            )

        if parent_post.is_deleted:
            raise HTTPException(
                status_code=409,
                detail="Impossible de répondre à un message supprimé",
            )

    post = ForumPost(
        topic_id=topic.id,
        author_id=current_user.id,
        parent_post_id=parent_post.id if parent_post else None,
        content=payload.content.strip(),
        is_edited=False,
    )
    db.add(post)

    topic.posts_count = int(topic.posts_count or 0) + 1

    topic_author_prefs = get_or_create_forum_notification_preferences(db, user_id=topic.author_id)
    if topic_author_prefs.notify_topic_replies:
        create_forum_notification(
            db,
            user_id=topic.author_id,
            actor_id=current_user.id,
            notification_type="topic_reply",
            title="Nouvelle réponse à votre sujet",
            message=f"{current_user.email} a répondu à « {topic.title} »",
            link=f"/forum/{topic.slug}",
        )

    participant_ids = db.execute(
        select(ForumPost.author_id)
        .where(
            ForumPost.topic_id == topic.id,
            ForumPost.is_deleted.is_(False),
            ForumPost.author_id != current_user.id,
            ForumPost.author_id != topic.author_id,
        )
        .distinct()
    ).scalars().all()

    for participant_id in participant_ids:
        prefs = get_or_create_forum_notification_preferences(db, user_id=participant_id)
        if prefs.notify_participated_topic_replies:
            create_forum_notification(
                db,
                user_id=participant_id,
                actor_id=current_user.id,
                notification_type="participated_topic_reply",
                title="Nouvelle activité dans un sujet suivi",
                message=f"{current_user.email} a répondu dans « {topic.title} »",
                link=f"/forum/{topic.slug}",
            )

    db.commit()
    db.refresh(post)

    stmt = (
        select(ForumPost)
        .options(
            joinedload(ForumPost.author),
            joinedload(ForumPost.parent_post).joinedload(ForumPost.author),
        )
        .where(ForumPost.id == post.id)
        .limit(1)
    )
    post = db.execute(stmt).scalar_one()

    return _serialize_post(post)


@router.put("/posts/{post_id}", response_model=ForumPostResponse)
def update_forum_post(
    post_id: UUID,
    payload: ForumPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_by_id(db, post_id)

    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    if post.is_deleted:
        raise HTTPException(status_code=409, detail="Impossible de modifier un message supprimé")

    revision = ForumPostRevision(
        post_id=post.id,
        editor_id=current_user.id,
        previous_content=post.content,
    )
    db.add(revision)

    post.content = payload.content.strip()
    post.is_edited = True

    db.commit()
    db.refresh(post)

    stmt = (
        select(ForumPost)
        .options(
            joinedload(ForumPost.author),
            joinedload(ForumPost.parent_post).joinedload(ForumPost.author),
        )
        .where(ForumPost.id == post.id)
        .limit(1)
    )
    post = db.execute(stmt).scalar_one()

    return _serialize_post(post)


@router.post("/posts/{post_id}/accept", response_model=ForumTopicModerationResponse)
def accept_forum_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_by_id(db, post_id)
    topic = post.topic

    if topic is None:
        raise HTTPException(status_code=500, detail="Sujet associé introuvable")

    if topic.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    if post.is_deleted:
        raise HTTPException(status_code=409, detail="Impossible de valider un message supprimé")

    topic.accepted_post_id = post.id

    post_author_prefs = get_or_create_forum_notification_preferences(db, user_id=post.author_id)
    if post_author_prefs.notify_accepted_answer:
        create_forum_notification(
            db,
            user_id=post.author_id,
            actor_id=current_user.id,
            notification_type="accepted_answer",
            title="Votre réponse a été retenue comme solution",
            message=f"{current_user.email} a marqué votre réponse comme solution sur « {topic.title} »",
            link=f"/forum/{topic.slug}",
        )

    db.commit()

    return ForumTopicModerationResponse(
        ok=True,
        topic_id=topic.id,
        accepted_post_id=topic.accepted_post_id,
    )


@router.post("/topics/{topic_id}/lock", response_model=ForumTopicModerationResponse)
def lock_forum_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    topic = _get_topic_by_id(db, topic_id)
    topic.is_locked = True
    db.commit()

    return ForumTopicModerationResponse(ok=True, topic_id=topic.id, is_locked=True)


@router.post("/topics/{topic_id}/unlock", response_model=ForumTopicModerationResponse)
def unlock_forum_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    topic = _get_topic_by_id(db, topic_id)
    topic.is_locked = False
    db.commit()

    return ForumTopicModerationResponse(ok=True, topic_id=topic.id, is_locked=False)


@router.post("/topics/{topic_id}/pin", response_model=ForumTopicModerationResponse)
def pin_forum_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    topic = _get_topic_by_id(db, topic_id)
    topic.is_pinned = True
    db.commit()

    return ForumTopicModerationResponse(ok=True, topic_id=topic.id, is_pinned=True)


@router.post("/topics/{topic_id}/unpin", response_model=ForumTopicModerationResponse)
def unpin_forum_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    topic = _get_topic_by_id(db, topic_id)
    topic.is_pinned = False
    db.commit()

    return ForumTopicModerationResponse(ok=True, topic_id=topic.id, is_pinned=False)


@router.delete("/posts/{post_id}")
def soft_delete_forum_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_by_id(db, post_id)

    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Action non autorisée")

    if post.is_deleted:
        return {"ok": True, "post_id": str(post.id), "is_deleted": True}

    post.is_deleted = True

    if post.topic is not None and post.topic.posts_count > 0:
        post.topic.posts_count -= 1

    if post.topic is not None and post.topic.accepted_post_id == post.id:
        post.topic.accepted_post_id = None

    stmt = select(ForumPost).where(ForumPost.parent_post_id == post.id)
    children = db.execute(stmt).scalars().all()
    for child in children:
        child.parent_post_id = None

    db.commit()

    return {"ok": True, "post_id": str(post.id), "is_deleted": True}


@router.post("/posts/{post_id}/vote", response_model=ForumVoteResponse)
def vote_forum_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_by_id(db, post_id)

    if post.is_deleted:
        raise HTTPException(status_code=409, detail="Impossible de voter pour un message supprimé")

    existing_vote = db.execute(
        select(ForumPostVote)
        .where(ForumPostVote.post_id == post.id, ForumPostVote.user_id == current_user.id)
        .limit(1)
    ).scalar_one_or_none()

    if existing_vote is not None:
        db.delete(existing_vote)
        if post.useful_votes_count > 0:
            post.useful_votes_count -= 1
        db.commit()
        return ForumVoteResponse(ok=True, post_id=post.id, useful_votes_count=post.useful_votes_count)

    vote = ForumPostVote(post_id=post.id, user_id=current_user.id)
    db.add(vote)
    post.useful_votes_count = int(post.useful_votes_count or 0) + 1
    db.commit()

    return ForumVoteResponse(ok=True, post_id=post.id, useful_votes_count=post.useful_votes_count)


@router.post("/posts/{post_id}/report", response_model=ForumReportResponse, status_code=status.HTTP_201_CREATED)
def report_forum_post(
    post_id: UUID,
    payload: ForumPostReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = _get_post_by_id(db, post_id)

    if post.is_deleted:
        raise HTTPException(status_code=409, detail="Impossible de signaler un message supprimé")

    report = ForumPostReport(
        post_id=post.id,
        reporter_id=current_user.id,
        reason=payload.reason.strip(),
        details=payload.details.strip() if payload.details else None,
        status="open",
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return ForumReportResponse(ok=True, report_id=report.id, post_id=post.id)