from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StreamFusionTokenCreateRequest(BaseModel):
    label: str | None = Field(default=None, max_length=120)


class StreamFusionTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    label: str | None = None
    created_at: datetime
    last_used_at: datetime | None = None
    revoked_at: datetime | None = None
    expires_at: datetime | None = None


class StreamFusionTokenCreateResponse(StreamFusionTokenResponse):
    plain_token: str
    configure_url: str


class StreamFusionTokenListResponse(BaseModel):
    items: list[StreamFusionTokenResponse]


class StreamFusionTokenActionResponse(BaseModel):
    ok: bool
    id: UUID