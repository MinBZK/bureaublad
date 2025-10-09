import logging
from functools import cache
from typing import Annotated

import httpx
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from jose.jws import get_unverified_header

from app.core.config import settings
from app.exceptions import CredentialError
from app.models.user import User

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(
    bearerFormat="JWT", scheme_name="Bearer", description="OpenID Connect JWT token", auto_error=True
)
openid_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=str(settings.OIDC_AUTHORIZATION_ENDPOINT),
    refreshUrl=str(settings.parsed_oidc_public_token_endpoint),
    tokenUrl=str(settings.parsed_oidc_public_token_endpoint),
    auto_error=False,
    scheme_name="OpenID Connect",
)


@cache
def get_public_key(kid: str) -> dict[str, str]:
    logger.debug(f"Fetching public key from {settings.OIDC_JWKS_ENDPOINT}")
    response = httpx.get(settings.OIDC_JWKS_ENDPOINT)
    response.raise_for_status()
    jwks = response.json()
    public_key = jwks["keys"][0]
    for key in jwks["keys"]:
        if key["kid"] == kid:
            public_key = key
            logger.debug("found matching public key")
            break
    return public_key


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
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    openid_token: str = Depends(openid_scheme),
) -> str:
    token = openid_token or (credentials.credentials if credentials else None)

    jtw_decode_options = {
        "require_iat": True,
        "require_exp": True,
        "require_iss": True,
        "require_sub": True,
        "require_jti": True,
    }

    try:
        # Get header info for key selection - signature verified in jwt.decode below
        header = get_unverified_header(token)  # NOSONAR
        alg = header.get("alg", None)
        _validate_jwt_algorithm(alg)

        # Determine verification key based on algorithm
        if alg == ALGORITHMS.RS256:
            kid = header.get("kid")
            key = get_public_key(kid=kid)
        else:
            key = str(settings.OIDC_CLIENT_SECRET)

        # Full signature verification happens here
        claims = jwt.decode(
            token,
            key,
            algorithms=settings.OIDC_SIGNATURE_ALGORITM,
            audience=settings.OIDC_AUDIENCE,
            issuer=settings.OIDC_ISSUER,
            options=jtw_decode_options,
        )
        sub: str = claims.get("sub", "unknown")
        name: str = claims.get("name", "unknown")
        email: str = claims.get("email", "unknown")
        request.state.user = User(sub=sub, access_token=token, name=name, email=email)

    except CredentialError:
        raise
    except JWTError as err:
        logger.exception("JWT validation failed")
        raise CredentialError("Invalid or expired JWT token") from err
    except httpx.HTTPError as err:
        logger.exception("Failed to fetch JWKS")
        raise CredentialError("Failed to validate credentials") from err
    except Exception as err:
        logger.exception("Authentication error")
        raise CredentialError("Authentication failed") from err

    return sub
