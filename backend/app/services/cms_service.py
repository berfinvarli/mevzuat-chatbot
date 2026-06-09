from app.persistence.cms_repository import CmsRepository


class CmsService:
    def __init__(self, repo: CmsRepository) -> None:
        self._repo = repo

    async def get(self, key: str) -> str | None:
        return await self._repo.get(key)

    async def get_all(self) -> dict[str, str]:
        return await self._repo.get_all()
