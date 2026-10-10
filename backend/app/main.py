from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.api.websocket import router as ws_router

app = FastAPI(
    title="Poly-Scan API",
    description="A static cross-language behavioral analysis tool API.",
    version="1.0.0"
)

# Configure CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local MVP dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/api/v1")
