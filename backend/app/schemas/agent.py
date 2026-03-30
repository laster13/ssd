from uuid import UUID

from pydantic import BaseModel


class AgentAuthResponse(BaseModel):
    authenticated: bool
    machine_id: UUID
    machine_uuid: UUID
    status: str