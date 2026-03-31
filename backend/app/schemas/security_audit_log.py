from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SecurityAuditLogItem(BaseModel):
    id: UUID
    event_type: str
    severity: str
    success: bool
    status_code: int | None = None
    actor_type: str | None = None
    actor_user_id: UUID | None = None
    actor_machine_id: UUID | None = None
    target_user_id: UUID | None = None
    target_machine_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    description: str | None = None
    details: dict | None = None
    created_at: datetime
