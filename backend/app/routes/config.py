import logging

from fastapi import APIRouter

from app.core.config import settings
from app.models.config import (
    ApplicationsConfig,
    ConfigResponse,
    SidebarLink,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/config", tags=["config"])


@router.get("")
async def get_config() -> ConfigResponse:
    sidebar_links = [SidebarLink(**link) for link in settings.SIDEBAR_LINKS_JSON]

    applications = ApplicationsConfig(
        ai=settings.ai_enabled,
        docs=settings.docs_enabled,
        drive=settings.drive_enabled,
        calendar=settings.calendar_enabled,
        task=settings.task_enabled,
        meet=settings.meet_enabled,
        ocs=settings.ocs_enabled,
        grist=settings.grist_enabled,
        conversation=settings.conversation_enabled,
    )

    return ConfigResponse(
        sidebar_links=sidebar_links,
        theme_css=settings.THEME_CSS_URL,
        applications=applications,
        silent_login=True,  # Backend handles authentication
    )
