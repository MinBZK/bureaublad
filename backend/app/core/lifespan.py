import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.const import VERSION
from app.core.redis import get_redis_client

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    logger.info(f"Starting version {VERSION}")

    try:
        redis_client = get_redis_client()
        await redis_client.ping()  # type: ignore[reportUnknownMemberType]
        logger.info("Successfully connected to Redis")
    except Exception:
        logger.exception("Failed to connect to Redis during startup")
    yield

    # Close the shared HTTP client to clean up connection pools
    from app.core.http_clients import http_client_dependency

    await http_client_dependency.aclose()

    logger.info(f"Stopping application version {VERSION}")
    logging.shutdown()
