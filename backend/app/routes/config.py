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

ALL_SERVICES = [
    "docs",
    "drive",
    "calendar",
    "task",
    "meet",
    "ocs",
    "grist",
    "conversation",
    "matrix",
    "projects",
    "email",
    "dictaphone",
]


@router.get("")
async def get_config(current_user: Annotated[User, Depends(get_current_user)]) -> ConfigResponse:
    """Get application configuration.
    Returns all configured services with a URL.
    """
    applications: list[ApplicationsConfig] = []

    for service_id in ALL_SERVICES:
        icon = getattr(settings, f"{service_id.upper()}_ICON", None)
        title = getattr(settings, f"{service_id.upper()}_TITLE", None)
        url = getattr(settings, f"{service_id.upper()}_URL", None)
        beta = getattr(settings, f"{service_id.upper()}_BETA", False)

        if url is not None:
            applications.append(
                ApplicationsConfig(
                    id=service_id,
                    icon=icon,
                    url=url,
                    title=title,
                    beta=beta,
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
