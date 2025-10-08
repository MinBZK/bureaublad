import httpx
from fastapi import APIRouter, HTTPException, status

from app.config import settings

router = APIRouter()


@router.get("/startup", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_startup() -> None:
    if not settings.OIDC_ISSUER or not settings.OIDC_JWKS_ENDPOINT:
        raise HTTPException(status_code=503, detail="Missing critical OIDC configuration")


@router.get("/readiness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_readiness() -> None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(settings.OIDC_JWKS_ENDPOINT)
            if response.status_code != 200:
                raise HTTPException(status_code=503, detail="OIDC provider not accessible")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Failed to connect to OIDC provider") from httpx.RequestError


@router.get("/liveness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_liveness() -> None:
    pass
