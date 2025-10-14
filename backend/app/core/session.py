"""AuthState session operations.

This module's responsibility: manage AuthState persistence in session storage.
Flow control (redirects, etc.) remains in routes.
"""

from fastapi import Request

from app.exceptions import CredentialError
from app.models.user import AuthState


def get_auth(request: Request) -> AuthState | None:
    """Get auth from session."""
    data = request.session.get("auth")
    return AuthState(**data) if data else None


def set_auth(request: Request, auth: AuthState) -> None:
    """Set auth in session."""
    request.session["auth"] = auth.model_dump()


def clear_auth(request: Request) -> None:
    """Clear auth from session."""
    request.session.pop("auth", None)


def update_tokens(
    request: Request,
    access_token: str,
    expires_at: int,
    refresh_token: str | None = None,
) -> None:
    """Update tokens in session after refresh.

    Note: This only updates token fields, not userinfo.
    """
    if "auth" not in request.session:
        raise CredentialError("No session to update")
    request.session["auth"]["access_token"] = access_token
    request.session["auth"]["expires_at"] = expires_at
    if refresh_token:
        request.session["auth"]["refresh_token"] = refresh_token
