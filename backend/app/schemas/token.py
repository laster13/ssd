from pydantic import BaseModel


class RotateMachineTokenResponse(BaseModel):
    ok: bool
    machine_token: str


class RevokeMachineTokenResponse(BaseModel):
    ok: bool
    machine_id: str
    status: str