from fastapi import FastAPI

from app.api.routes.admin import router as admin_router
from app.api.routes.agent import router as agent_router
from app.api.routes.auth import router as auth_router
from app.api.routes.bootstrap import router as bootstrap_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.me import router as me_router
from app.api.routes.pairing import router as pairing_router
from app.api.routes.streamfusion import router as streamfusion_router
from app.api.routes.ws import router as ws_router

app = FastAPI(title="SSD Backend")

app.include_router(auth_router)
app.include_router(pairing_router)
app.include_router(agent_router)
app.include_router(admin_router)
app.include_router(ws_router)
app.include_router(bootstrap_router)
app.include_router(me_router)
app.include_router(streamfusion_router)
app.include_router(catalog_router)