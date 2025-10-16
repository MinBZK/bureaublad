import logging

import httpx

from app.core.config import settings
from app.exceptions import CredentialError

logger = logging.getLogger(__name__)


async def exchange_token(
    http_client: httpx.AsyncClient,
    token: str,
    audience: str,
    subject_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    requested_token_type: str = "urn:ietf:params:oauth:token-type:access_token",  # noqa: S107
    scope: str = "openid",
) -> str | None:
    """Exchange an access token for a new token with different audience.

    Implements RFC 8693 OAuth 2.0 Token Exchange with Keycloak.

    Args:
        token: The subject access token to exchange
        audience: Target audience for the new token (e.g., 'files', 'docs')
        subject_token_type: Type of the subject token (default: access_token)
        requested_token_type: Type of token to receive (default: access_token)
        scope: OAuth scopes for the new token

    Returns:
        The exchanged access token, or None if exchange fails

    Raises:
        CredentialError: If token exchange fails due to configuration or permission issues
    """
    # TODO: Add caching with TTL based on token expiration to reduce
    # Keycloak load. For now, we exchange fresh tokens for every request.

    try:
        logger.info(f"Exchanging token for audience={audience}")
        logger.info(f"Token exchange request: {token}")

        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": token,
            "subject_token_type": subject_token_type,
            "requested_token_type": requested_token_type,
            "scope": scope,
            "audience": audience,
        }

        response = await http_client.post(
            settings.OIDC_TOKEN_ENDPOINT,
            data=data,
            auth=(settings.OIDC_CLIENT_ID, settings.OIDC_CLIENT_SECRET or ""),
        )

        if response.status_code == 400:
            logger.error(f"Token exchange failed with 400: {response.text}")
            raise CredentialError("Unable to authenticate. Please try logging in again.")

        if response.status_code == 401:
            logger.warning(f"Token exchange failed with 401: {response.text}")
            raise CredentialError("Your session has expired. Please log in again.")

        if response.status_code == 403:
            logger.warning(f"Token exchange forbidden for {audience=}: {response.text}")
            raise CredentialError("Access denied. You may not have permission to access this service.")

        # Raise for any other HTTP errors
        response.raise_for_status()

        token_data = response.json()
        exchanged_token: str = token_data["access_token"]
        logger.info(f"Token exchange response: {exchanged_token}")
        logger.info(f"Successfully exchanged token for audience={audience}")

    except httpx.HTTPError as e:
        logger.exception("Token exchange failed due to network error")
        raise CredentialError("Authentication service unavailable") from e
    except KeyError as e:
        logger.exception("Token exchange response missing access_token")
        raise CredentialError("Invalid token exchange response") from e
    else:
        return exchanged_token
