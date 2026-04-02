from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, StringConstraints, conint

JobLogMessage = Annotated[str, StringConstraints(min_length=1, max_length=4000)]


class AgentCreateJobLogRequest(BaseModel):
    seq: conint(ge=0)
    level: Literal["debug", "info", "warning", "error"] = "info"
    message: JobLogMessage


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