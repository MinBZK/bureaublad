import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.authentication import get_current_user
from app.config import settings
from app.lifespan import lifespan
from app.routes.main import api_router
from app.routes.root import router as root_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

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

app.include_router(api_router, dependencies=[Depends(get_current_user)], prefix=settings.API_V1_STR)
app.include_router(root_router, tags=["health"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
