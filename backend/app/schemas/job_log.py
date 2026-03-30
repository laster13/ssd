from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AgentCreateJobLogRequest(BaseModel):
    seq: int
    level: str = "info"
    message: str


class AgentCreateJobLogResponse(BaseModel):
    ok: bool
    log_id: UUID
    job_id: UUID
    seq: int


class AdminJobLogItem(BaseModel):
    id: UUID
    job_id: UUID
    seq: int
    level: str
    message: str
    created_at: datetime
