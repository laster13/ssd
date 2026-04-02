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


def extract_ws_token(websocket: WebSocket) -> str | None:
    authorization = websocket.headers.get("authorization")
    if authorization:
        parts = authorization.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1].strip()

    token = websocket.query_params.get("token")
    if token:
        return token.strip()

    return None


@router.websocket("/ws/jobs/{job_id}")
async def websocket_job_logs(websocket: WebSocket, job_id: UUID):
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
    try:
        user = db.execute(
            select(User).where(User.id == subject).limit(1)
        ).scalar_one_or_none()

        if not user or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        job = db.execute(
            select(Job)
            .join(Machine, Machine.id == Job.machine_id)
            .where(Job.id == job_id)
            .limit(1)
        ).scalar_one_or_none()

        if not job:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        machine = db.execute(
            select(Machine).where(Machine.id == job.machine_id).limit(1)
        ).scalar_one_or_none()

        if not machine:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if not user.is_admin and machine.owner_id != user.id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await job_ws_manager.connect(job_id, websocket)

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            job_ws_manager.disconnect(job_id, websocket)
        except Exception:
            job_ws_manager.disconnect(job_id, websocket)
    finally:
        db.close()