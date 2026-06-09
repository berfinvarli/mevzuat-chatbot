from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.persistence.models import CmsEntry
from app.persistence.postgres import get_sessionmaker


class CmsRepository:
    def __init__(
        self, sessionmaker: async_sessionmaker[AsyncSession] | None = None
    ) -> None:
        self._sessionmaker = sessionmaker or get_sessionmaker()

    async def get_all(self) -> dict[str, str]:
        async with self._sessionmaker() as session:
            result = await session.execute(select(CmsEntry.key, CmsEntry.value))
            return {key: value for key, value in result.all()}

    async def get(self, key: str) -> str | None:
        async with self._sessionmaker() as session:
            row = await session.get(CmsEntry, key)
            return row.value if row else None

    async def seed_defaults(self, defaults: dict[str, str]) -> None:
        if not defaults:
            return
        rows = [{"key": key, "value": value} for key, value in defaults.items()]
        stmt = insert(CmsEntry).values(rows).on_conflict_do_nothing(index_elements=["key"])
        async with self._sessionmaker() as session:
            await session.execute(stmt)
            await session.commit()
