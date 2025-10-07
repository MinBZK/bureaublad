import logging

import httpx

from bureaublad_api.core.config import settings
from bureaublad_api.exceptions import TokenExchangeError

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

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=settings.OIDC_TOKEN_ENDPOINT,
            data=payload,
            headers=headers,
        )

    logger.debug(f"Token exchange response status: {response.status_code}")
    if response.status_code != 200:
        logger.error(f"Token exchange failed: status={response.status_code}, response={response.text}")
        raise TokenExchangeError(f"Token exchange failed with status {response.status_code}")

    return response.json().get("access_token", None)
