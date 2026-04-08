from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ApplicationStateResponse(BaseModel):
    id: UUID
    machine_id: UUID
    app_slug: str
    app_name: str | None = None

    present: bool
    transition: str

    last_operation: str | None = None
    last_job_id: UUID | None = None
    last_job_status: str | None = None
    last_error: str | None = None

    installed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    # nouveau champ calculé à la volée
    public_url: str | None = None