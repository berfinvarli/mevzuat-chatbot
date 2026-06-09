from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING

from app.core.config import settings
from app.core.constants import CONVERSATIONS_COLLECTION, MONGODB_DB

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_url)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    return get_client()[MONGODB_DB]


async def create_indexes() -> None:
    db = get_db()
    await db[CONVERSATIONS_COLLECTION].create_index(
        [("session_id", ASCENDING), ("created_at", ASCENDING)]
    )
