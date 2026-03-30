from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PairingRegisterResponse(BaseModel):
    machine_id: UUID
    machine_uuid: UUID
    pairing_code: str
    expires_at: datetime


class PairingVerifyRequest(BaseModel):
    pairing_code: str


class PairingVerifyResponse(BaseModel):
    valid: bool
    machine_id: UUID | None = None
    machine_uuid: UUID | None = None
    status: str | None = None
    machine_token: str | None = None