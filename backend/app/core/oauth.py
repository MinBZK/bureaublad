from authlib.integrations.starlette_client import OAuth  # type: ignore[reportMissingTypeStubs]

from app.core.config import settings

oauth = OAuth()

oauth.register(  # type: ignore[reportUnknownMemberType]
    name="oidc",
    issuer=settings.OIDC_ISSUER,
    client_id=settings.OIDC_CLIENT_ID,
    client_secret=settings.OIDC_CLIENT_SECRET,
    access_token_url=settings.OIDC_TOKEN_ENDPOINT,
    authorize_url=settings.OIDC_AUTHORIZATION_ENDPOINT,
    jwks_uri=settings.OIDC_JWKS_ENDPOINT,
    audience=settings.OIDC_AUDIENCE,
    revocation_endpoint=settings.OIDC_REVOCATION_ENDPOINT,  # RFC 7009 token revocation
    client_kwargs={
        "scope": settings.OIDC_SCOPES,
        "code_challenge_method": "S256",  # Enable PKCE with SHA-256
    },
)
