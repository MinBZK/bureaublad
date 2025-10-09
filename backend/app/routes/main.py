from fastapi import APIRouter

from app.routes import ai, caldav, config, docs, drive, meet, ocs

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(ocs.router)
api_router.include_router(caldav.router)
api_router.include_router(ai.router)
api_router.include_router(config.router)
api_router.include_router(drive.router)
api_router.include_router(meet.router)
