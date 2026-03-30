from pydantic import BaseModel


class RotateMachineTokenResponse(BaseModel):
    ok: bool
    machine_token: str
