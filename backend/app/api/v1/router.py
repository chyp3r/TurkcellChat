from fastapi import APIRouter
from app.api.v1.endpoints import chat, ingest, root, master_agent

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

api_router.include_router(master_agent.router, prefix="/agent", tags=["Agent"])

api_router.include_router(ingest.router, prefix="/ingest", tags=["Upload"])

api_router.include_router(root.router, tags=["Root"])

