import logging
from typing import cast

import httpx
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import ExceptionHandler

from app.const import VERSION
from app.core.authentication import get_current_user
from app.core.config import settings
from app.core.exception_handlers import (
    generic_exception_handler,
    http_exception_handler,
    httpx_exception_handler,
    validation_exception_handler,
)
from app.core.lifespan import lifespan
from app.core.logging import configure_logging
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.routes.authentication import router as auth_router
from app.routes.health import router as health_router
from app.routes.main import api_router

configure_logging(settings.LOGGING_LEVEL, settings.LOGGING_CONFIG)

logger = logging.getLogger(__name__)
logger.info(f"Bureaublad API starting - Log level: {settings.LOGGING_LEVEL}, Environment: {settings.ENVIRONMENT}")


app = FastAPI(
    title="Bureaublad API",
    summary="API for portal resources",
    debug=settings.DEBUG,
    version=VERSION,
    redirect_slashes=False,
    openapi_url="/openapi.json",
    docs_url="/",
    redoc_url=None,
    lifespan=lifespan,
    servers=[
        {"url": "http://localhost:8000", "description": "local environment"},
    ],
    license_info={"name": "EUPL1.2", "url": "https://opensource.org/license/eupl-1-2"},
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": -1,
        "docExpansion": "none",
        "filter": "true",
        "tagsSorter": "alpha",
        "validatorUrl": None,
        "persistAuthorization": True,
    },
)

# Register exception handlers
app.add_exception_handler(HTTPException, cast(ExceptionHandler, http_exception_handler))
app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, validation_exception_handler))
app.add_exception_handler(httpx.HTTPError, cast(ExceptionHandler, httpx_exception_handler))
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router, prefix=settings.API_V1_STR)  # No auth required for auth endpoints
app.include_router(api_router, dependencies=[Depends(get_current_user)], prefix=settings.API_V1_STR)
app.include_router(health_router, tags=["health"])

# Middleware execution order (reverse of add order):
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session",
    max_age=settings.SESSION_MAX_AGE,
    same_site="lax",
    https_only=settings.ENVIRONMENT == "prod",  # Only require HTTPS in production
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)

if settings.ENVIRONMENT == "prod":
    app.add_middleware(HTTPSRedirectMiddleware)
