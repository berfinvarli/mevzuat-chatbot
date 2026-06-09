from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.constants import RATE_LIMIT
from app.core.limiter import limiter
from app.persistence.conversation_repository import ConversationRepository, SessionId
from app.persistence.mongo import get_db
from app.schemas.chat_request import ChatRequest
from app.services.chat_service import ChatService
from app.services.mcp_service import MCPService
from app.services.runtime_settings_service import runtime_settings_service

chat_router = APIRouter()


def get_chat_service() -> ChatService:
    return ChatService(
        openai_client=AsyncOpenAI(api_key=settings.openai_api_key),
        mcp_service=MCPService(url=settings.mcp_server_url),
        settings_service=runtime_settings_service,
        repo=ConversationRepository(get_db()),
    )


@chat_router.post("/chat")
@limiter.limit(RATE_LIMIT)
async def chat(
    request: Request,
    body: ChatRequest,
    session_id: SessionId | None = Cookie(default=None),
    service: ChatService = Depends(get_chat_service),
):
    return StreamingResponse(
        service.stream(body.messages, session_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@chat_router.get("/history")
async def get_history(
    session_id: SessionId | None = Cookie(default=None),
    service: ChatService = Depends(get_chat_service),
):
    if not session_id:
        return {"messages": []}
    return {"messages": await service.get_history(session_id)}


@chat_router.get("/health")
async def health():
    rs = await runtime_settings_service.get()
    return {"status": "ok", "model": rs.openai_model, "mcp_url": settings.mcp_server_url}
