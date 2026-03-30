from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.ws import job_ws_manager

router = APIRouter(tags=["ws"])


@router.websocket("/ws/jobs/{job_id}")
async def websocket_job_logs(websocket: WebSocket, job_id: UUID):
    await job_ws_manager.connect(job_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        job_ws_manager.disconnect(job_id, websocket)
    except Exception:
        job_ws_manager.disconnect(job_id, websocket)
