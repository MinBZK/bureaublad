from fastapi import APIRouter

from app.routes import config, search

api_router = APIRouter()
api_router.include_router(config.router)
api_router.include_router(search.router)
