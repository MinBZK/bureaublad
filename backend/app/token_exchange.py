import logging

import httpx
from jose import jwt

from app.config import settings

logger = logging.getLogger(__name__)


async def exchange_token(
    token: str,
    audience: str,
    subject_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    requested_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    scope: str = "openid profile email",
) -> dict:
    unverified_claims = jwt.get_unverified_claims(token)
    print(unverified_claims)
    # check if audiance is already in claim. if so, no need to exchange token
    if "aud" in unverified_claims:
        audience_unverified_claim = unverified_claims["aud"]
        print(audience_unverified_claim)
        if isinstance(audience_unverified_claim, list) and audience in audience_unverified_claim:
            return token
        if isinstance(audience_unverified_claim, str) and audience_unverified_claim == audience:
            return token

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

        logger.debug(response.status_code)
        new_token = response.json().get("access_token", None)

        return new_token
