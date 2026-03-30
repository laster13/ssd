from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AgentMeResponse(BaseModel):
    machine_id: UUID
    machine_uuid: UUID
    status: str
    hostname: str | None = None
    agent_version: str | None = None
    auth_token_created_at: datetime | None = None
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
