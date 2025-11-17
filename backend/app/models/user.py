import logging
from typing import Any, cast

from pydantic import BaseModel

from app.core.translate import _
from app.exceptions import CredentialError

logger = logging.getLogger(__name__)


class User(BaseModel):
    name: str
    email: str


class AuthState(BaseModel):
    """Authentication state from OAuth."""

    sub: str
    user: User
    access_token: str
    refresh_token: str | None = None
    expires_at: int | None = None

    @classmethod
    def from_token(cls, token: dict[str, Any], name_claim: str, email_claim: str) -> "AuthState":
        """Construct AuthState from OAuth token response."""
        userinfo = cls._get_userinfo(token)

        return cls(
            sub=cls._require_string(userinfo, "sub"),
            user=User(
                name=userinfo.get(name_claim, "Unknown"),
                email=userinfo.get(email_claim, "no-email@unknown.local"),
            ),
            access_token=cls._require_string(token, "access_token"),
            refresh_token=token.get("refresh_token"),
            expires_at=token.get("expires_at"),
        )

    @staticmethod
    def _get_userinfo(token: dict[str, Any]) -> dict[str, Any]:
        userinfo = token.get("userinfo")
        if not userinfo or not isinstance(userinfo, dict):
            raise CredentialError(_("Missing userinfo in token"))
        return cast(dict[str, Any], userinfo)

    @staticmethod
    def _require_string(data: dict[str, Any], key: str) -> str:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise CredentialError(_(f"Missing or invalid {key}"))
        return value
