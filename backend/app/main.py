import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.authentication import get_current_user
from app.config import settings
from app.const import VERSION
from app.lifespan import lifespan
from app.middleware.logging import RequestLoggingMiddleware
from app.routes.main import api_router
from app.routes.root import router as root_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

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
    swagger_ui_init_oauth={
        "clientId": settings.OIDC_CLIENT_ID,
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": "openid profile email",
    },
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

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router, tags=["health"])

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
