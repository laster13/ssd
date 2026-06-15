from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

ErrorMessage = Annotated[str, StringConstraints(max_length=4000)]


class CreateMachineJobRequest(BaseModel):
    app_slug: str
    subdomain: str
    auth_type: str
    app_config: dict[str, Any] = Field(default_factory=dict)


class CreateMachineJobResponse(BaseModel):
    job_id: UUID
    machine_id: UUID
    status: str
    type: str
    payload: dict | None = None


class CreateMyInstallationRequest(BaseModel):
    machine_id: UUID
    app_slug: str
    subdomain: str
    auth_type: str
    app_config: dict[str, Any] = Field(default_factory=dict)


class AgentFetchJobResponse(BaseModel):
    has_job: bool
    job_id: UUID | None = None
    type: str | None = None
    payload: dict | None = None
    status: str | None = None
    claimed_at: datetime | None = None


class AgentCompleteJobRequest(BaseModel):
    result: dict | None = None
    error_message: ErrorMessage | None = None


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
    payload: dict | None = None
    created_at: datetime
    updated_at: datetime