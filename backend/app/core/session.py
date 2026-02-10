"""AuthState session operations.

This module's responsibility: manage AuthState persistence in session storage.
Flow control (redirects, etc.) remains in routes.
"""

import json
import uuid

from fastapi import Request

from app.core.redis import get_redis_client
from app.exceptions import CredentialError
from app.models.user import AuthState


def _redis_key(request: Request) -> str | None:
    """Build a Redis key for the current session."""
    session_id = request.session.get("session_id")
    return f"auth:{session_id}" if session_id else None


async def get_auth(request: Request) -> AuthState | None:
    """Get auth from session."""

    key = _redis_key(request)
    if not key:
        return None

    redis_client = get_redis_client()
    data = await redis_client.get(key)
    data_dict = json.loads(data) if data else None

    if data_dict:
        return AuthState.model_validate(data_dict)
    return None


async def set_auth(request: Request, auth: AuthState) -> str:
    """Set auth in session."""

    key = request.session["session_id"] if "session_id" in request.session else str(uuid.uuid4())

    payload = auth.model_dump()

    redis_client = get_redis_client()
    await redis_client.set(f"auth:{key}", json.dumps(payload))
    request.session["session_id"] = key
    return key


async def clear_auth(request: Request) -> None:
    """Clear auth from session."""

    key = _redis_key(request)
    if key:
        redis_client = get_redis_client()
        await redis_client.delete(key)
        request.session.pop("session_id", None)


async def update_tokens(
    request: Request,
    access_token: str,
    expires_at: int,
    refresh_token: str | None = None,
) -> None:
    """Update tokens in session after refresh.

    Note: This only updates token fields, not userinfo.
    """

    auth = await get_auth(request)

    if not auth:
        raise CredentialError("No auth state found for session")

    auth.access_token = access_token
    auth.expires_at = expires_at
    if refresh_token:
        auth.refresh_token = refresh_token

    await set_auth(request, auth)
