from fastapi import APIRouter

from app.api.admin_settings import admin_router
from app.api.chat import chat_router
from app.api.cms import cms_router

api_router = APIRouter()
api_router.include_router(chat_router)
api_router.include_router(cms_router)
api_router.include_router(admin_router)
