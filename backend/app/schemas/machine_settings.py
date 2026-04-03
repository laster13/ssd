from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MachineSettingsResponse(BaseModel):
    machine_id: UUID
    username: str | None = None
    email: str | None = None
    domain: str | None = None
    password: str | None = None
    cloudflare_login: str | None = None
    cloudflare_api_key: str | None = None
    oauth_enabled: bool = False
    oauth_client: str | None = None
    oauth_secret: str | None = None
    oauth_mail: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UpdateMachineSettingsRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    domain: str | None = None
    password: str | None = None
    cloudflare_login: str | None = None
    cloudflare_api_key: str | None = None
    oauth_enabled: bool = False
    oauth_client: str | None = None
    oauth_secret: str | None = None
    oauth_mail: str | None = None