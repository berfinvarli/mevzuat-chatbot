import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.persistence.models import AppSettings
from app.persistence.postgres import get_sessionmaker
from app.schemas.runtime_settings import RuntimeSettings

logger = logging.getLogger(__name__)

_SETTINGS_ID = 1
_FIELDS = (
    "system_prompt",
    "openai_model",
    "temperature",
    "max_tokens",
    "max_tool_iterations",
    "stream_token_delay",
)


class SettingsRepository:
    def __init__(
        self, sessionmaker: async_sessionmaker[AsyncSession] | None = None
    ) -> None:
        self._sessionmaker = sessionmaker or get_sessionmaker()

    async def get(self) -> RuntimeSettings | None:
        async with self._sessionmaker() as session:
            row = await session.get(AppSettings, _SETTINGS_ID)
            if row is None:
                return None
            return RuntimeSettings.model_validate(
                {f: getattr(row, f) for f in _FIELDS}
            )

    async def upsert(self, values: dict, updated_by: str | None = None) -> RuntimeSettings:
        async with self._sessionmaker() as session:
            row = await session.get(AppSettings, _SETTINGS_ID)
            if row is None:
                base = RuntimeSettings.defaults().model_dump()
                base.update(values)
                row = AppSettings(id=_SETTINGS_ID, updated_by=updated_by, **base)
                session.add(row)
            else:
                for key, value in values.items():
                    setattr(row, key, value)
                row.updated_by = updated_by
            await session.commit()
            return RuntimeSettings.model_validate(
                {f: getattr(row, f) for f in _FIELDS}
            )
