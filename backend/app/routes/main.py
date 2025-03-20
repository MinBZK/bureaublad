from fastapi import APIRouter

from app.routes import ai, caldav, docs, nextcloud

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(nextcloud.router)
api_router.include_router(caldav.router)
api_router.include_router(ai.router)
