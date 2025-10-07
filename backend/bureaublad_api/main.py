import logging
from typing import cast

import httpx
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.types import ExceptionHandler

from bureaublad_api.core.authentication import get_current_user
from bureaublad_api.core.config import settings
from bureaublad_api.core.exception_handlers import (
    generic_exception_handler,
    http_exception_handler,
    httpx_exception_handler,
    validation_exception_handler,
)
from bureaublad_api.core.lifespan import lifespan
from bureaublad_api.core.logging import configure_logging
from bureaublad_api.middleware.logging import RequestLoggingMiddleware
from bureaublad_api.routes.health import router as health_router
from bureaublad_api.routes.main import api_router

configure_logging(settings.LOGGING_LEVEL, settings.LOGGING_CONFIG)

logger = logging.getLogger(__name__)
logger.info(f"Bureaublad API starting - Log level: {settings.LOGGING_LEVEL}, Environment: {settings.ENVIRONMENT}")


app = FastAPI(
    title="Bureaublad API",
    debug=settings.DEBUG,
    version="0.1.0",
    redirect_slashes=False,
    openapi_url="/openapi.json",
    docs_url="/",
    redoc_url=None,
    lifespan=lifespan,
)

# Register exception handlers
app.add_exception_handler(HTTPException, cast(ExceptionHandler, http_exception_handler))
app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, validation_exception_handler))
app.add_exception_handler(httpx.HTTPError, cast(ExceptionHandler, httpx_exception_handler))
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(api_router, dependencies=[Depends(get_current_user)], prefix=settings.API_V1_STR)
app.include_router(health_router, tags=["health"])

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
