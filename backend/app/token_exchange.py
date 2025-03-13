import logging

import httpx

from app.config import settings

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

    response = httpx.post(
        url=settings.OIDC_TOKEN_ENDPOINT,
        data=payload,
        headers=headers,
    )

    logger.debug(response.status_code)
    if response.status_code != 200:
        logger.debug(response.text)

    new_token = response.json().get("access_token", None)

    return new_token
