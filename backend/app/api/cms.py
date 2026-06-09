from fastapi import APIRouter, Depends, HTTPException, status

from app.persistence.cms_repository import CmsRepository
from app.services.cms_service import CmsService

cms_router = APIRouter()


def get_cms_service() -> CmsService:
    return CmsService(CmsRepository())


@cms_router.get("/cms")
async def get_cms(
    service: CmsService = Depends(get_cms_service),
) -> dict[str, str]:
    return await service.get_all()


@cms_router.get("/cms/{key}")
async def get_cms_value(
    key: str,
    service: CmsService = Depends(get_cms_service),
) -> dict[str, str]:
    value = await service.get(key)
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CMS anahtarı bulunamadı: {key}",
        )
    return {"key": key, "value": value}
