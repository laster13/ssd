from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateMachineJobRequest(BaseModel):
    app_slug: str
    subdomain: str
    auth_type: str


class CreateMachineJobResponse(BaseModel):
    job_id: UUID
    machine_id: UUID
    status: str
    type: str
    payload: dict | None = None


class AgentFetchJobResponse(BaseModel):
    has_job: bool
    job_id: UUID | None = None
    type: str | None = None
    payload: dict | None = None
    status: str | None = None
    claimed_at: datetime | None = None


class AgentCompleteJobRequest(BaseModel):
    result: dict | None = None
    error_message: str | None = None


class AgentCompleteJobResponse(BaseModel):
    ok: bool
    job_id: UUID
    status: str
    completed_at: datetime


class AdminJobResponse(BaseModel):
    id: UUID
    machine_id: UUID
    type: str
    status: str
    payload: dict | None = None
    result: dict | None = None
    error_message: str | None = None
    claimed_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AdminJobListItem(BaseModel):
    id: UUID
    machine_id: UUID
    type: str
    status: str
    created_at: datetime
    updated_at: datetime