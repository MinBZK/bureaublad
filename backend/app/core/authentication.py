import logging

from fastapi import Request

from app.core.config import settings
from app.exceptions import CredentialError
from app.models.user import User

logger = logging.getLogger(__name__)


def _validate_jwt_algorithm(alg: str | None) -> None:
    """Validate that the JWT algorithm is in the allowed list."""
    allowed_algorithms = (
        settings.OIDC_SIGNATURE_ALGORITM
        if isinstance(settings.OIDC_SIGNATURE_ALGORITM, list)
        else [settings.OIDC_SIGNATURE_ALGORITM]
    )
    if alg not in allowed_algorithms:
        raise CredentialError(f"Unsupported JWT algorithm: {alg}")


def get_current_user(
    request: Request,
) -> str:
    sub: str = "test-sub"
    name: str = "Test User"
    email: str = "test@example.com"
    token: str = "test-token"  # noqa: S105

    sub: str = "unknown"
    name: str = "unknown"
    email: str = "unknown"
    request.state.user = User(sub=sub, access_token=token, name=name, email=email)

    return sub
