from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StreamFusionTokenCreateRequest(BaseModel):
    label: str | None = None


class StreamFusionTokenCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    label: str | None = None
    created_at: datetime
    last_used_at: datetime | None = None
    revoked_at: datetime | None = None
    expires_at: datetime | None = None
    plain_token: str
    configure_url: str