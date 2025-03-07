from fastapi import APIRouter

from app.routes import docs

api_router = APIRouter()
api_router.include_router(docs.router)
