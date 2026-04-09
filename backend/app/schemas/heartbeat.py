from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AgentInstalledApplication(BaseModel):
    app_slug: str
    app_name: str | None = None
    public_url: str | None = None


class AgentHeartbeatRequest(BaseModel):
    hostname: str | None = None
    agent_version: str | None = None
    ssdv2_installed: bool | None = None
    installed_apps: list[AgentInstalledApplication] | None = None


class AgentHeartbeatResponse(BaseModel):
    ok: bool
    machine_id: UUID
    machine_uuid: UUID
    status: str
    last_seen_at: datetime
