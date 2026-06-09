import logging

from app.persistence.settings_repository import SettingsRepository
from app.schemas.runtime_settings import RuntimeSettings, RuntimeSettingsUpdate

logger = logging.getLogger(__name__)


class RuntimeSettingsService:
    def __init__(self, repo: SettingsRepository | None = None) -> None:
        self._repo = repo or SettingsRepository()
        self._cache: RuntimeSettings | None = None

    async def get(self) -> RuntimeSettings:
        if self._cache is not None:
            return self._cache
        try:
            loaded = await self._repo.get()
        except Exception:
            logger.exception("Postgre'den ayarlar okunamadı, env default kullanılıyor")
            loaded = None
        self._cache = loaded or RuntimeSettings.defaults()
        return self._cache

    async def update(
        self, patch: RuntimeSettingsUpdate, updated_by: str | None = None
    ) -> RuntimeSettings:
        values = patch.model_dump(exclude_unset=True)
        updated = await self._repo.upsert(values, updated_by=updated_by)
        self._cache = updated
        return updated

    def invalidate(self) -> None:
        self._cache = None


runtime_settings_service = RuntimeSettingsService()
