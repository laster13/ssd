from urllib.parse import urlparse
from uuid import UUID

import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy import select

from app.core.auth import decode_access_token
from app.core.database import SessionLocal
from app.core.security import hash_machine_token
from app.core.ws import job_ws_manager, machine_presence_manager
from app.models.job import Job
from app.models.machine import Machine
from app.models.user import User

router = APIRouter(tags=["ws"])

TOKEN_COOKIE_NAME = "token"

ALLOWED_WS_ORIGINS = {
    "https://ssd.lastharo.eu",
    "https://panel.lastharo.eu",
}

LOCALHOST_HOSTS = {"localhost", "127.0.0.1"}


def is_allowed_browser_origin(websocket: WebSocket) -> bool:
    origin = websocket.headers.get("origin")
    if not origin:
        return False

    if origin in ALLOWED_WS_ORIGINS:
        return True

    parsed = urlparse(origin)
    return parsed.scheme in {"http", "https"} and parsed.hostname in LOCALHOST_HOSTS


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


def serialize_machine(machine: Machine, *, connection_status: str) -> dict:
    return {
        "id": str(machine.id),
        "machine_uuid": str(machine.machine_uuid),
        "status": machine.status,
        "connection_status": connection_status,
        "hostname": machine.hostname,
        "agent_version": machine.agent_version,
        "ssdv2_installed": getattr(machine, "ssdv2_installed", None),
        "ssdv2_checked_at": machine.ssdv2_checked_at.isoformat()
        if getattr(machine, "ssdv2_checked_at", None)
        else None,
        "last_seen_at": machine.last_seen_at.isoformat() if machine.last_seen_at else None,
        "created_at": machine.created_at.isoformat() if machine.created_at else None,
        "updated_at": machine.updated_at.isoformat() if machine.updated_at else None,
    }


def build_machine_presence_event(machine: Machine, *, connection_status: str) -> dict:
    return {
        "type": "machine_presence",
        "machine": serialize_machine(machine, connection_status=connection_status),
    }


async def authenticate_ws_user(websocket: WebSocket, db) -> User | None:
    token = extract_ws_token(websocket)
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    subject = payload.get("sub")
    if not subject:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    user = db.execute(select(User).where(User.id == subject).limit(1)).scalar_one_or_none()
    if not user or not user.is_active:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    return user


async def authenticate_ws_machine(websocket: WebSocket, machine_id: UUID, db) -> Machine | None:
    token = extract_ws_token(websocket)
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    token_hash = hash_machine_token(token)
    machine = db.execute(
        select(Machine)
        .where(Machine.id == machine_id)
        .where(Machine.auth_token_hash == token_hash)
        .limit(1)
    ).scalar_one_or_none()

    if not machine or machine.status == "revoked":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    return machine


@router.websocket("/ws/jobs/{job_id}")
async def websocket_job_logs(websocket: WebSocket, job_id: UUID):
    if not is_allowed_browser_origin(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db = SessionLocal()
    connected = False

    try:
        user = await authenticate_ws_user(websocket, db)
        if not user:
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


@router.websocket("/ws/machines")
async def websocket_my_machines(websocket: WebSocket):
    if not is_allowed_browser_origin(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db = SessionLocal()
    connected = False
    user: User | None = None

    try:
        user = await authenticate_ws_user(websocket, db)
        if not user:
            return

        await machine_presence_manager.connect_user(user.id, websocket)
        connected = True

        machines = db.execute(
            select(Machine)
            .where(Machine.owner_id == user.id)
            .where(Machine.status == "paired")
            .order_by(Machine.created_at.desc())
        ).scalars().all()

        await websocket.send_json(
            {
                "type": "machine_snapshot",
                "machines": [
                    serialize_machine(
                        machine,
                        connection_status=(
                            "online"
                            if machine_presence_manager.is_machine_online(machine.id)
                            else "offline"
                        ),
                    )
                    for machine in machines
                ],
            }
        )

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    finally:
        if connected and user:
            machine_presence_manager.disconnect_user(user.id, websocket)
        db.close()


@router.websocket("/ws/admin/machines")
async def websocket_admin_machines(websocket: WebSocket):
    if not is_allowed_browser_origin(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    db = SessionLocal()
    connected = False

    try:
        user = await authenticate_ws_user(websocket, db)
        if not user:
            return

        if not user.is_admin:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await machine_presence_manager.connect_admin(websocket)
        connected = True

        machines = db.execute(select(Machine).order_by(Machine.created_at.desc())).scalars().all()

        await websocket.send_json(
            {
                "type": "machine_snapshot",
                "machines": [
                    serialize_machine(
                        machine,
                        connection_status=(
                            "online"
                            if machine.status != "revoked"
                            and machine_presence_manager.is_machine_online(machine.id)
                            else "offline"
                        ),
                    )
                    for machine in machines
                ],
            }
        )

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    finally:
        if connected:
            machine_presence_manager.disconnect_admin(websocket)
        db.close()


@router.websocket("/ws/machines/{machine_id}/agent")
async def websocket_machine_agent_presence(websocket: WebSocket, machine_id: UUID):
    db = SessionLocal()
    connected = False
    machine: Machine | None = None

    try:
        machine = await authenticate_ws_machine(websocket, machine_id, db)
        if not machine:
            return

        became_online = await machine_presence_manager.connect_agent(machine.id, websocket)
        connected = True

        if became_online:
            event = build_machine_presence_event(machine, connection_status="online")
            if machine.owner_id:
                await machine_presence_manager.broadcast_to_user(machine.owner_id, event)
            await machine_presence_manager.broadcast_to_admins(event)

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    finally:
        if connected and machine:
            became_offline = machine_presence_manager.disconnect_agent(machine.id, websocket)
            if became_offline:
                refreshed_machine = db.execute(
                    select(Machine).where(Machine.id == machine.id).limit(1)
                ).scalar_one_or_none() or machine
                event = build_machine_presence_event(refreshed_machine, connection_status="offline")
                if machine.owner_id:
                    await machine_presence_manager.broadcast_to_user(machine.owner_id, event)
                await machine_presence_manager.broadcast_to_admins(event)
        db.close()
