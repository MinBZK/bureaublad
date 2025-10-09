from fastapi import APIRouter, status

router = APIRouter()


@router.get("/startup", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_startup() -> None:
    # Startup probe - indicates application has started successfully
    # Returns 204 immediately as application is ready once FastAPI initializes
    pass


@router.get("/readiness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_readyness() -> None:
    # Readiness probe - indicates application is ready to accept traffic
    # TODO: check identity provider connection before returning success
    pass


@router.get("/liveness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_liveness() -> None:
    # Liveness probe - indicates application is alive and not deadlocked
    # Returns 204 immediately as ability to respond indicates process is healthy
    pass
