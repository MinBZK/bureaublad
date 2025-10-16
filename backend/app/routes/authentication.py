import logging
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

from app.core import session
from app.core.config import settings
from app.core.oauth import oauth
from app.exceptions import CredentialError
from app.models.user import AuthState, User

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login(request: Request, redirect_to: str | None = None) -> RedirectResponse:
    """
    Initiate OAuth 2.0 Authorization Code Flow with PKCE.

    Authlib automatically handles:
    - CSRF protection via 'state' parameter (generated and validated)
    - PKCE code_verifier/code_challenge generation and storage
    """
    if redirect_to:
        # Validate redirect_to to prevent open redirect vulnerability
        if not _is_safe_redirect(redirect_to):
            raise CredentialError("Invalid redirect URL")
        request.session["redirect_to"] = redirect_to
    else:
        request.session["redirect_to"] = settings.OIDC_POST_LOGIN_REDIRECT_URI

    redirect_uri = request.url_for("callback")

    return await oauth.oidc.authorize_redirect(request, redirect_uri)  # type: ignore[reportUnknownMemberType, reportUnknownVariableType]


@router.get("/callback")
async def callback(request: Request) -> RedirectResponse:
    """Handle OAuth 2.0 callback and exchange authorization code for tokens."""
    try:
        token: dict[str, Any] = await oauth.oidc.authorize_access_token(request)  # type: ignore[reportUnknownMemberType]

        auth = AuthState.from_token(token, name_claim=settings.OIDC_NAME_CLAIM, email_claim=settings.OIDC_EMAIL_CLAIM)  # type: ignore[reportUnknownArgumentType]
        session.set_auth(request, auth)  # type: ignore[reportUnknownArgumentType]

        redirect_to = request.session.pop("redirect_to", "/")
        logger.info(f"User {auth.sub} authenticated successfully")  # type: ignore[reportUnknownMemberType]
        return RedirectResponse(url=redirect_to, status_code=302)

    except Exception:
        logger.exception("OAuth callback failed")
        # Clear any partial session state
        request.session.pop("redirect_to", None)
        # Redirect to login with error parameter instead of raising exception
        error_message = "authentication_failed"
        return RedirectResponse(url=f"/login?error={error_message}", status_code=302)


@router.get("/profile")
async def profile(request: Request) -> User:
    """Get current user profile from session."""
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    return auth.user


@router.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    """Clear session and perform RP-initiated logout with token revocation."""
    auth = session.get_auth(request)

    # Revoke refresh token before clearing session (best effort, RFC 7009)
    if auth and auth.refresh_token and settings.OIDC_REVOCATION_ENDPOINT:
        try:
            # Get OAuth2 client and call revoke_token
            # Note: revoke_token() is not declared async but returns a coroutine
            # because AsyncOAuth2Client._http_post() returns self.post() without await
            async with oauth.oidc._get_oauth_client() as client:  # type: ignore[reportUnknownMemberType, reportUnknownVariableType]
                await client.revoke_token(  # type: ignore[reportUnknownMemberType]
                    url=settings.OIDC_REVOCATION_ENDPOINT,
                    token=auth.refresh_token,
                    token_type_hint="refresh_token",  # noqa: S106
                )
            logger.info(f"Revoked refresh token for user {auth.sub}")  # type: ignore[reportUnknownMemberType]
        except Exception:
            logger.warning("Token revocation failed during logout", exc_info=True)

    session.clear_auth(request)
    return RedirectResponse(_build_logout_url())


def _is_safe_redirect(url: str) -> bool:
    """Validate that redirect URL is safe (relative or https)."""
    if not url:
        return False

    # Allow relative URLs (start with /) and HTTPS URLs.
    # Block absolute and protocol-relative URLs.
    # TODO: Add domain whitelist validation for absolute URLs.
    return url.startswith("https://") or (url.startswith("/") and not url.startswith("//"))


def _build_logout_url() -> str:
    """Build OIDC logout URL with required parameters."""
    if not settings.OIDC_POST_LOGOUT_REDIRECT_URI:
        raise CredentialError("OIDC_POST_LOGOUT_REDIRECT_URI must be configured")

    logout_url = URL(settings.OIDC_LOGOUT_ENDPOINT)
    return str(
        logout_url.include_query_params(
            post_logout_redirect_uri=settings.OIDC_POST_LOGOUT_REDIRECT_URI,
            client_id=settings.OIDC_CLIENT_ID,
        )
    )
