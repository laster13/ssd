from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import Request

from app.core.database import SessionLocal
from app.models.security_audit_log import SecurityAuditLog


def get_request_ip(request: Request | None) -> str | None:
    if not request:
        return None

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return None


def get_request_user_agent(request: Request | None) -> str | None:
    if not request:
        return None
    return request.headers.get("user-agent")


def audit_event(
    *,
    event_type: str,
    severity: str = "info",
    success: bool = True,
    status_code: int | None = None,
    actor_type: str | None = None,
    actor_user_id: UUID | None = None,
    actor_machine_id: UUID | None = None,
    target_user_id: UUID | None = None,
    target_machine_id: UUID | None = None,
    request: Request | None = None,
    description: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    db = SessionLocal()
    try:
        log = SecurityAuditLog(
            event_type=event_type,
            severity=severity,
            success=success,
            status_code=status_code,
            actor_type=actor_type,
            actor_user_id=actor_user_id,
            actor_machine_id=actor_machine_id,
            target_user_id=target_user_id,
            target_machine_id=target_machine_id,
            ip_address=get_request_ip(request),
            user_agent=get_request_user_agent(request),
            description=description,
            details=details,
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
