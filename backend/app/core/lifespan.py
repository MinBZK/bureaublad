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

    # Close the shared HTTP client to clean up connection pools
    from app.core.http_clients import http_client_dependency

    await http_client_dependency.aclose()

    logger.info(f"Stopping application version {VERSION}")
    logging.shutdown()
