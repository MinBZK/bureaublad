import logging

from fastapi import Request

from app.core import session
from app.core.config import settings
from app.exceptions import CredentialError

logger = logging.getLogger(__name__)


async def exchange_token(
    token: str,
    audience: str,
    subject_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    requested_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    scope: str = "openid profile email",
) -> str | None:
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "client_id": settings.OIDC_CLIENT_ID,
        "subject_token": token,
        "subject_token_type": subject_token_type,
        "requested_token_type": requested_token_type,
        "audience": audience,
        "scope": scope,
    }
    if settings.OIDC_CLIENT_SECRET:
        payload.update({"client_secret": settings.OIDC_CLIENT_SECRET})

    if settings.OIDC_ISSUER:
        payload.update({"subject_issuer": settings.OIDC_ISSUER})

    return token


async def get_token(request: Request, audience: str) -> str:
    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    return await exchange_token(auth.access_token, audience=audience) or ""
