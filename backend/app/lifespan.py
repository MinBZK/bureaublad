import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.const import VERSION

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    logger.info(f"Starting version {VERSION}")
    yield

    logger.info(f"Stopping application version {VERSION}")
    logging.shutdown()
