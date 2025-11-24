import logging
from typing import cast

from fastapi import APIRouter

from app.core.config import settings
from app.models.config import (
    ApplicationsConfig,
    ConfigResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/config", tags=["config"])

ALL_SERVICES = ["ai", "docs", "drive", "calendar", "task", "meet", "ocs", "grist", "conversation"]


@router.get("")
async def get_config() -> ConfigResponse:
    """Get application configuration.

    Returns all enabled services. If a service is in SIDEBAR_LINKS_JSON,
    uses those display values (icon, url, title). Otherwise uses None.
    """
    # Create lookup for sidebar link customizations
    sidebar_links_by_id = {cast(str, link["id"]): link for link in settings.SIDEBAR_LINKS_JSON}

    applications: list[ApplicationsConfig] = []

    for service_id in ALL_SERVICES:
        # Check if service is enabled
        enabled = getattr(settings, f"{service_id}_enabled", False)

        if enabled:
            # Get customization from SIDEBAR_LINKS_JSON if present
            link = sidebar_links_by_id.get(service_id, {})

            applications.append(
                ApplicationsConfig(
                    id=service_id,
                    enabled=enabled,
                    icon=cast(str | None, link.get("icon")),
                    url=cast(str | None, link.get("url")),
                    title=cast(str | None, link.get("title")),
                    iframe=cast(bool, link.get("iframe", False)),
                )
            )

    return ConfigResponse(
        applications=applications,
        theme_css=settings.THEME_CSS_URL,
        silent_login=True,  # Backend handles authentication
    )
