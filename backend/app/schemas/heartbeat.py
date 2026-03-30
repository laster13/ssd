from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AgentHeartbeatRequest(BaseModel):
    hostname: str | None = None
    agent_version: str | None = None


class AgentHeartbeatResponse(BaseModel):
    ok: bool
    machine_id: UUID
    machine_uuid: UUID
    status: str
    last_seen_at: datetime
