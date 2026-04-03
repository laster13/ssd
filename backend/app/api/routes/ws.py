from uuid import UUID

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy import select

from app.core.auth import decode_access_token
from app.core.database import SessionLocal
from app.core.ws import job_ws_manager
from app.models.job import Job
from app.models.machine import Machine
from app.models.user import User

router = APIRouter(tags=["ws"])

TOKEN_COOKIE_NAME = "token"

ALLOWED_WS_ORIGINS = {
    "https://ssd.lastharo.eu",
    "https://panel.lastharo.eu",
}


def is_allowed_origin(websocket: WebSocket) -> bool:
    origin = websocket.headers.get("origin")
    return origin in ALLOWED_WS_ORIGINS


def extract_ws_token(websocket: WebSocket) -> str | None:
    authorization = websocket.headers.get("authorization")
    if authorization:
        parts = authorization.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1].strip()
            if token:
                return token

    token = websocket.query_params.get("token")
    if token:
        token = token.strip()
        if token:
            return token

    cookie_token = websocket.cookies.get(TOKEN_COOKIE_NAME)
    if cookie_token:
        cookie_token = cookie_token.strip()
        if cookie_token:
            return cookie_token

    return None


@router.websocket("/ws/jobs/{job_id}")
async def websocket_job_logs(websocket: WebSocket, job_id: UUID):
    if not is_allowed_origin(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    token = extract_ws_token(websocket)
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    subject = payload.get("sub")
    if not subject:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db = SessionLocal()
    connected = False

    try:
        user = db.execute(
            select(User).where(User.id == subject).limit(1)
        ).scalar_one_or_none()

        if not user or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        row = db.execute(
            select(Job, Machine)
            .join(Machine, Machine.id == Job.machine_id)
            .where(Job.id == job_id)
            .limit(1)
        ).first()

        if not row:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        job, machine = row

        if not user.is_admin and machine.owner_id != user.id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await job_ws_manager.connect(job_id, websocket)
        connected = True

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    finally:
        if connected:
            job_ws_manager.disconnect(job_id, websocket)
        db.close()