from fastapi import APIRouter

from app.routes import docs, nextcloud

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(nextcloud.router)
