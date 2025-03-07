from fastapi import status
from fastapi.exceptions import HTTPException


class CredentialError(HTTPException):
    def __init__(self) -> None:
        self.detail: str = "Could not validate credentials"
        self.headers: dict[str, str] = {"Authenticate": "Bearer"}
        super().__init__(status.HTTP_401_UNAUTHORIZED, self.detail)
