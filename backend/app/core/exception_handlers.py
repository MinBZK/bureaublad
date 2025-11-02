import logging

import httpx
from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle all HTTPException instances and return standardized error response.

    Returns response in format: {"msg": "error message"}
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"msg": exc.detail},
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle request validation errors and return detailed error information.

    Returns response in format: {"msg": "summary", "errors": [...]}
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "msg": "Validation error",
            "errors": exc.errors(),
        },
    )


async def httpx_exception_handler(request: Request, exc: httpx.HTTPError) -> JSONResponse:
    """
    Handle httpx HTTP errors (connection errors, timeouts, etc.).

    Returns 502 Bad Gateway for external service errors.
    """
    logger.error(f"External service error: {exc.__class__.__name__}: {exc}")

    if isinstance(exc, httpx.TimeoutException):
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"msg": "External service timeout"},
        )

    if isinstance(exc, httpx.ConnectError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"msg": "External service unavailable"},
        )

    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"msg": "External service error"},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unhandled exceptions.

    Returns 500 Internal Server Error and logs the full exception.
    """
    logger.exception(f"Unhandled exception: {exc.__class__.__name__}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"msg": "Internal server error"},
    )
