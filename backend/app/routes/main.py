from fastapi import APIRouter

from app.routes import config

api_router = APIRouter()
api_router.include_router(config.router)

