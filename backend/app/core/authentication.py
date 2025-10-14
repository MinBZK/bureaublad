import asyncio
import logging
import time

from fastapi import Request

from app.core import session
from app.core.oauth import oauth
from app.exceptions import CredentialError
from app.models.user import User

logger = logging.getLogger(__name__)

# Global lock to prevent concurrent token refreshes for the same session
_refresh_locks: dict[str, asyncio.Lock] = {}


async def get_current_user(request: Request) -> User:
    """Get authenticated user, refreshing token if needed."""
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    if _needs_refresh(auth.expires_at):
        # Use session ID as lock key to prevent concurrent refreshes for same session
        session_id = request.session.get("_session_id", id(request.session))

        # Get or create lock for this session
        if session_id not in _refresh_locks:
            _refresh_locks[session_id] = asyncio.Lock()

        lock = _refresh_locks[session_id]

        async with lock:
            # Re-check after acquiring lock (another request may have refreshed)
            auth = session.get_auth(request)
            if not auth:
                raise CredentialError("Not authenticated")

            # Only refresh if still needed (another request may have already refreshed)
            if _needs_refresh(auth.expires_at):
                await _refresh_token(request, auth.refresh_token)
                auth = session.get_auth(request)
                if not auth:
                    raise CredentialError("Session lost after refresh")

        # Clean up lock after refresh to prevent memory leak
        _refresh_locks.pop(session_id, None)

    request.state.user = auth.user
    return auth.user


def _needs_refresh(expires_at: int | None) -> bool:
    """Check if token needs refresh (expired or expiring within 60s)."""
    if not expires_at:
        return False
    return int(time.time()) >= expires_at - 60


async def _refresh_token(request: Request, refresh_token: str | None) -> None:
    """Refresh access token using refresh token."""
    if not refresh_token:
        logger.warning("No refresh token available")
        raise CredentialError("Session expired. Please log in again.")

    try:
        logger.info("Refreshing access token")
        token = await oauth.oidc.fetch_token(  # type: ignore[reportUnknownMemberType]
            grant_type="refresh_token",
            refresh_token=refresh_token,
        )

        session.update_tokens(
            request,
            access_token=str(token["access_token"]),  # type: ignore[reportUnknownArgumentType]
            expires_at=int(token["expires_at"]),  # type: ignore[reportUnknownArgumentType]
            refresh_token=token.get("refresh_token"),  # type: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        )

        logger.info("Access token refreshed successfully")
    except Exception as e:
        logger.exception("Token refresh failed")
        session.clear_auth(request)
        raise CredentialError("Session expired. Please log in again.") from e
