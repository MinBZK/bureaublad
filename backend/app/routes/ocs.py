import logging

from fastapi import APIRouter, Request

from app.clients.ocs import OCSClient
from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import CredentialError, ServiceUnavailableError
from app.models.activity import Activity
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocs", tags=["ocs"])


@router.get("/activities", response_model=list[Activity])
async def ocs_activities(
    request: Request,
    http_client: HTTPClient,
) -> list[Activity]:
    """Get activities from OCS service.

    Note: Auth is validated by get_current_user() at router level.
    """
    if not settings.ocs_enabled or not settings.OCS_URL:
        raise ServiceUnavailableError("OCS")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.OCS_AUDIENCE) or ""

    client = OCSClient(http_client, settings.OCS_URL, token)
    return await client.get_activities()
