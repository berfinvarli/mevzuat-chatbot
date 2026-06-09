import logging
from datetime import datetime, timezone
from typing import NewType

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.constants import CONVERSATIONS_COLLECTION
from app.schemas.message import Message

SessionId = NewType("SessionId", str)

logger = logging.getLogger(__name__)


class ConversationRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._col = db[CONVERSATIONS_COLLECTION]

    async def get_messages(self, session_id: SessionId) -> list[dict]:
        try:
            cursor = self._col.find(
                {"session_id": session_id},
                {"_id": 0, "role": 1, "content": 1, "created_at": 1},
                sort=[("created_at", 1)],
            )
            return await cursor.to_list(length=None)
        except Exception:
            logger.exception("MongoDB konuşma geçmişi okunamadı: session_id=%s", session_id)
            return []

    async def append_messages(self, session_id: SessionId, messages: list[Message]) -> None:
        now = datetime.now(timezone.utc)
        docs = [
            {"session_id": session_id, "role": m.role, "content": m.content, "created_at": now}
            for m in messages
        ]
        await self._col.insert_many(docs)
