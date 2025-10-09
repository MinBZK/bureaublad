from fastapi import status
from fastapi.exceptions import HTTPException


class CredentialError(HTTPException):
    """Raised when authentication credentials are invalid or missing."""

    def __init__(self, detail: str = "Could not validate credentials") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExchangeError(HTTPException):
    """Raised when token exchange with the identity provider fails."""

    def __init__(self, detail: str = "Token exchange failed") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ServiceUnavailableError(HTTPException):
    """Raised when a required service is not configured or unavailable."""

    def __init__(self, service: str) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{service} service is not configured",
        )


class ExternalServiceError(HTTPException):
    """Raised when an external service returns an error."""

    def __init__(self, service: str, detail: str | None = None) -> None:
        message = f"{service} service error"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=message)


class NotFoundError(HTTPException):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource} not found")


class BadRequestError(HTTPException):
    """Raised when the request is malformed or invalid."""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
