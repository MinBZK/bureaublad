from fastapi import APIRouter, status

router = APIRouter()


@router.get("/startup", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_startup() -> None:
    pass


@router.get("/readiness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_readyness() -> None:
    # todo: check identity provider connection
    pass


@router.get("/liveness", status_code=status.HTTP_204_NO_CONTENT)
async def root_get_liveness() -> None:
    pass
