import logging

import httpx
from fastapi import Request

from app.core import session
from app.core.config import settings
from app.core.translate import _
from app.exceptions import CredentialError, TokenExchangeError

logger = logging.getLogger(__name__)


async def exchange_token(
    token: str,
    audience: str,
    subject_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    requested_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    scope: str = "openid",
) -> str | None:
    logger.info(f"Exchanging token for audience={audience}")

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "subject_token": token,
        "subject_token_type": subject_token_type,
        "requested_token_type": requested_token_type,
        "scope": scope,
        "audience": audience,
    }

    response = httpx.post(  # todo reuse http_client
        settings.OIDC_TOKEN_ENDPOINT,
        data=data,
        auth=(settings.OIDC_CLIENT_ID, settings.OIDC_CLIENT_SECRET or ""),
    )

    if response.status_code == 400:
        logger.error(f"Token exchange failed with 400 for audience={audience}")
        raise CredentialError("Unable to authenticate. Please try logging in again.")

    if response.status_code == 401:
        logger.warning(f"Token exchange failed with 401 for audience={audience}")
        raise CredentialError("Your session has expired. Please log in again.")

    if response.status_code == 403:
        logger.warning(f"Token exchange forbidden for audience={audience}")
        raise CredentialError("Access denied. You may not have permission to access this service.")

    # Raise for any other HTTP errors
    response.raise_for_status()

    try:
      token_data = response.json()
    except Exception:
      logger.error(f"Token exchange returned non-JSON response for audience={audience}")
      raise TokenExchangeError("Token exchange returned an invalid response. Please try logging in again.")

    exchanged_token = token_data.get("access_token")

    if not exchanged_token or not isinstance(exchanged_token, str):
      logger.error(f"Token exchange response missing 'access_token' for audience={audience}")
      raise TokenExchangeError("Token exchange returned an invalid response. Please try logging in again.")


    logger.info(f"Successfully exchanged token for audience={audience}")

    return exchanged_token


async def get_token(request: Request, audience: str) -> str:
    # Get auth from session (already refreshed by get_current_user dependency)
    auth = await session.get_auth(request)
    if not auth:
        raise CredentialError(_("Not authenticated"))

    return await exchange_token(token=auth.access_token, audience=audience) or ""
