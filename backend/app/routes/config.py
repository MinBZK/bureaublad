import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.authentication import get_current_user
from app.core.config import settings
from app.models.config import (
    ApplicationsConfig,
    ConfigResponse,
)
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/config", tags=["config"])

ALL_SERVICES = ["ai", "docs", "drive", "calendar", "task", "meet", "ocs", "grist", "conversation", "matrix"]


@router.get("")
async def get_config(current_user: Annotated[User, Depends(get_current_user)]) -> ConfigResponse:
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

    is_admin = settings.ADMIN_ROLE_NAME in current_user.roles

    return ConfigResponse(
        applications=applications,
        theme_css=settings.THEME_CSS_URL,
        helpdesk_url=settings.HELPDESK_URL,
        redirect_to_account_page=settings.REDIRECT_TO_ACCOUNT_PAGE,
        silent_login=True,  # Backend handles authentication
        is_admin=is_admin,
    )
