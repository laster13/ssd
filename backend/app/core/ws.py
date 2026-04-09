from collections import defaultdict
from uuid import UUID

from fastapi import WebSocket


class JobConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, job_id: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[str(job_id)].append(websocket)

    def disconnect(self, job_id: UUID, websocket: WebSocket) -> None:
        job_key = str(job_id)
        if job_key in self.connections:
            self.connections[job_key] = [
                conn for conn in self.connections[job_key] if conn is not websocket
            ]
            if not self.connections[job_key]:
                del self.connections[job_key]

    async def broadcast(self, job_id: UUID, payload: dict) -> None:
        job_key = str(job_id)
        if job_key not in self.connections:
            return

        dead_connections: list[WebSocket] = []

        for websocket in self.connections[job_key]:
            try:
                await websocket.send_json(payload)
            except Exception:
                dead_connections.append(websocket)

        for websocket in dead_connections:
            self.disconnect(job_id, websocket)


class MachinePresenceConnectionManager:
    def __init__(self) -> None:
        self.agent_connections: dict[str, list[WebSocket]] = defaultdict(list)
        self.user_connections: dict[str, list[WebSocket]] = defaultdict(list)
        self.admin_connections: list[WebSocket] = []

    def is_machine_online(self, machine_id: UUID | str) -> bool:
        return bool(self.agent_connections.get(str(machine_id)))

    async def connect_agent(self, machine_id: UUID | str, websocket: WebSocket) -> bool:
        await websocket.accept()
        machine_key = str(machine_id)
        was_online = self.is_machine_online(machine_key)
        self.agent_connections[machine_key].append(websocket)
        return not was_online

    def disconnect_agent(self, machine_id: UUID | str, websocket: WebSocket) -> bool:
        machine_key = str(machine_id)
        if machine_key not in self.agent_connections:
            return False

        self.agent_connections[machine_key] = [
            conn for conn in self.agent_connections[machine_key] if conn is not websocket
        ]

        if self.agent_connections[machine_key]:
            return False

        del self.agent_connections[machine_key]
        return True

    async def close_agent_connections(self, machine_id: UUID | str, code: int = 1000) -> None:
        machine_key = str(machine_id)
        connections = list(self.agent_connections.get(machine_key, []))

        for websocket in connections:
            try:
                await websocket.close(code=code)
            except Exception:
                pass

        if machine_key in self.agent_connections:
            del self.agent_connections[machine_key]

    async def connect_user(self, user_id: UUID | str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.user_connections[str(user_id)].append(websocket)

    def disconnect_user(self, user_id: UUID | str, websocket: WebSocket) -> None:
        user_key = str(user_id)
        if user_key not in self.user_connections:
            return

        self.user_connections[user_key] = [
            conn for conn in self.user_connections[user_key] if conn is not websocket
        ]

        if not self.user_connections[user_key]:
            del self.user_connections[user_key]

    async def broadcast_to_user(self, user_id: UUID | str, payload: dict) -> None:
        user_key = str(user_id)
        if user_key not in self.user_connections:
            return

        dead_connections: list[WebSocket] = []

        for websocket in self.user_connections[user_key]:
            try:
                await websocket.send_json(payload)
            except Exception:
                dead_connections.append(websocket)

        for websocket in dead_connections:
            self.disconnect_user(user_key, websocket)

    async def connect_admin(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.admin_connections.append(websocket)

    def disconnect_admin(self, websocket: WebSocket) -> None:
        self.admin_connections = [conn for conn in self.admin_connections if conn is not websocket]

    async def broadcast_to_admins(self, payload: dict) -> None:
        if not self.admin_connections:
            return

        dead_connections: list[WebSocket] = []

        for websocket in self.admin_connections:
            try:
                await websocket.send_json(payload)
            except Exception:
                dead_connections.append(websocket)

        for websocket in dead_connections:
            self.disconnect_admin(websocket)


job_ws_manager = JobConnectionManager()
machine_presence_manager = MachinePresenceConnectionManager()
