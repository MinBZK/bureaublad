import logging

from fastapi import APIRouter

from app.core.config import settings
from app.models.config import (
    ApplicationsConfig,
    ConfigResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/config", tags=["config"])

ALL_SERVICES = ["ai", "docs", "drive", "calendar", "task", "meet", "ocs", "grist", "conversation", "matrix"]


@router.get("")
async def get_config() -> ConfigResponse:
    """Get application configuration.
    Returns all enabled services.
    """
    applications: list[ApplicationsConfig] = []

    for service_id in ALL_SERVICES:
        # Check if service is enabled
        enabled = getattr(settings, f"{service_id.upper()}_CARD", False)
        icon = getattr(settings, f"{service_id.upper()}_ICON", None)
        title = getattr(settings, f"{service_id.upper()}_TITLE", None)
        url = getattr(settings, f"{service_id.upper()}_URL", None)
        iframe = getattr(settings, f"{service_id.upper()}_IFRAME", False)

        if url is not None:
            applications.append(
                ApplicationsConfig(
                    id=service_id,
                    enabled=enabled,
                    icon=icon,
                    url=url,
                    title=title,
                    iframe=iframe,
                )
            )

    return ConfigResponse(
        applications=applications,
        theme_css=settings.THEME_CSS_URL,
        helpdesk_url=settings.HELPDESK_URL,
        silent_login=True,  # Backend handles authentication
    )
