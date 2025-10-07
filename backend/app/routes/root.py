import httpx
from fastapi import APIRouter, status

from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ExternalServiceError, ServiceUnavailableError

router = APIRouter()


@router.get("/startup", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_startup() -> None:
    if not settings.OIDC_ISSUER or not settings.OIDC_JWKS_ENDPOINT:
        raise ServiceUnavailableError("OIDC")


@router.get("/readiness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_readiness(http_client: HTTPClient) -> None:
    try:
        response = await http_client.get(settings.OIDC_JWKS_ENDPOINT)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise ExternalServiceError("OIDC provider", f"HTTP {e.response.status_code}") from e
    except httpx.RequestError as e:
        raise ExternalServiceError("OIDC provider", "Connection failed") from e


@router.get("/liveness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_liveness() -> None:
    pass
