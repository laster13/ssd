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


job_ws_manager = JobConnectionManager()
