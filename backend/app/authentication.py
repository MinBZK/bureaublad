import logging
from functools import cache
from typing import Annotated

import httpx
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from jose.jws import get_unverified_header

from app.config import settings
from app.exception import CredentialError
from app.models import User

logger = logging.getLogger(__name__)

security = HTTPBearer(bearerFormat="JWT", scheme_name="bearer", description="OpenID Connect JWT token", auto_error=True)


@cache
def get_public_key(kid: str) -> dict[str, str]:
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


def get_current_user(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    token = credentials.credentials

    jtw_decode_options = {
        "require_iat": True,
        "require_exp": True,
        "require_iss": True,
        "require_sub": True,
        "require_jti": True,
    }

    try:
        header = get_unverified_header(token)
        alg = header.get("alg", None)

        if alg == ALGORITHMS.RS256:
            kid = header.get("kid")
            key = get_public_key(kid=kid)
        else:
            key = str(settings.OIDC_CLIENT_SECRET)

        claims = jwt.decode(
            token,
            key,
            algorithms=settings.OIDC_SIGNATURE_ALGORITM,
            audience=settings.OIDC_AUDIENCE,
            issuer=settings.OIDC_ISSUER,
            options=jtw_decode_options,
        )
        sub: str = claims.get("sub", "unknown")
        request.state.user = User(sub=sub, access_token=token)

    except JWTError as err:
        logger.debug("JWTError")
        raise CredentialError from err
    except Exception as err:
        logger.debug("Exception authentication")
        raise CredentialError from err

    return sub
