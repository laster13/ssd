from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AdminMachineListItem(BaseModel):
    id: UUID
    machine_uuid: UUID
    status: str
    connection_status: str | None = None
    hostname: str | None = None
    agent_version: str | None = None
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AdminMachineResponse(BaseModel):
    id: UUID
    machine_uuid: UUID
    status: str
    connection_status: str | None = None
    hostname: str | None = None
    agent_version: str | None = None
    auth_token_created_at: datetime | None = None
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
