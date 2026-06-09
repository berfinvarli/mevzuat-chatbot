import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.router import api_router
from app.core.constants import API_V1_PREFIX, DEFAULT_CMS
from app.core.middleware import setup_middleware
from app.persistence.cms_repository import CmsRepository
from app.persistence.mongo import create_indexes
from app.persistence.postgres import create_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await create_indexes()
    await create_tables()
    await CmsRepository().seed_defaults(DEFAULT_CMS)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Mevzuat Chatbot API", lifespan=lifespan)

    setup_middleware(app)
    app.include_router(api_router, prefix=API_V1_PREFIX)

    return app
