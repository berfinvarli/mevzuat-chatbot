import secrets

from fastapi import APIRouter, Header, HTTPException, status

from app.core.config import settings
from app.schemas.runtime_settings import RuntimeSettings, RuntimeSettingsUpdate
from app.services.runtime_settings_service import runtime_settings_service

admin_router = APIRouter(prefix="/admin")


def _require_admin(x_admin_token: str | None) -> None:
    expected = settings.admin_token
    if not x_admin_token or not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz admin token",
        )


@admin_router.get("/settings", response_model=RuntimeSettings)
async def get_settings(x_admin_token: str | None = Header(default=None)) -> RuntimeSettings:
    _require_admin(x_admin_token)
    return await runtime_settings_service.get()


@admin_router.put("/settings", response_model=RuntimeSettings)
async def update_settings(
    patch: RuntimeSettingsUpdate,
    x_admin_token: str | None = Header(default=None),
) -> RuntimeSettings:
    _require_admin(x_admin_token)
    return await runtime_settings_service.update(patch, updated_by="admin")
