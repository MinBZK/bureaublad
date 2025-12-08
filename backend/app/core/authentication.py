import logging
import time
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.core import session
from app.core.config import settings
from app.core.oauth import oauth
from app.core.translate import _
from app.exceptions import CredentialError, TokenRefreshConflictError
from app.models.user import User

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/api/v1/auth/login",
    tokenUrl=settings.OIDC_TOKEN_ENDPOINT,
    auto_error=False,
)


async def get_current_user(
    request: Request, _credentials: Annotated[OAuth2AuthorizationCodeBearer, Depends(oauth2_scheme)]
) -> User:
    """Get authenticated user, refreshing token if needed.
    _credentials is unused but required to trigger OAuth2 flow in the swagger UI.
    """

    auth = session.get_auth(request)

    if not auth:
        raise CredentialError(_("Not authenticated"))

    if _needs_refresh(auth.expires_at):
        await _refresh_token(request, auth.refresh_token)

        # Re-read auth to get updated tokens
        auth = session.get_auth(request)
        if not auth:
            raise CredentialError(_("Session expired. Please log in again."))

    request.state.user = auth.user
    return auth.user


def _needs_refresh(expires_at: int | None) -> bool:
    """Check if token needs refresh (expired or expiring within 60s)."""
    if not expires_at:
        return False
    return int(time.time()) >= expires_at - 60


async def _refresh_token(request: Request, refresh_token: str | None) -> None:
    """Perform OAuth token refresh and update the session."""
    if not refresh_token:
        logger.warning("No refresh token available")
        raise CredentialError(_("Session expired. Please log in again."))

    try:
        logger.info("Refreshing access token via OAuth")
        token = await oauth.oidc.fetch_access_token(  # type: ignore[reportUnknownMemberType]
            grant_type="refresh_token",
            refresh_token=refresh_token,
        )

        logger.info("Access token refreshed successfully")

        # Update session with new tokens
        session.update_tokens(
            request,
            access_token=str(token["access_token"]),  # type: ignore[reportUnknownArgumentType]
            expires_at=int(token["expires_at"]),  # type: ignore[reportUnknownArgumentType]
            refresh_token=token.get("refresh_token"),  # type: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        )

        logger.info("Refreshed access token updated successfully")

    except Exception as e:
        error_str = str(e).lower()

        # Check if this is a "refresh token reuse" error from Keycloak
        # This happens when concurrent requests try to refresh the same token.
        if "maximum allowed refresh token reuse exceeded" in error_str:
            logger.warning(f"Refresh token conflict detected. Token already used by concurrent request: {e}")
            raise TokenRefreshConflictError("Refresh token already used") from e

        # Check if this is an expired/inactive token (expected session expiration)
        if "token is not active" in error_str or "token expired" in error_str:
            logger.info(f"Session expired - token no longer valid: {e}")
            session.clear_auth(request)
            raise CredentialError(_("Session expired. Please log in again.")) from e

        # Other unexpected OAuth errors (corrupted session, network issues, etc.)
        logger.exception("Unexpected OAuth token refresh error")
        session.clear_auth(request)
        raise CredentialError(_("Session expired. Please log in again.")) from e
