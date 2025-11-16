from typing import Optional

from fastapi import HTTPException, status
from starlette.responses import JSONResponse


class UnauthenticatedException(HTTPException):
    _status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "Bad Request"):
        self.message = message
        super().__init__(status_code=self._status_code, detail=message)

    @classmethod
    def throw(cls, message: Optional[str] = None):
        raise cls(message=message or "Your are not authenticated")


def unauthenticated_exception_handler(exc: UnauthenticatedException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "errors": [], "status": exc.status_code},
    )
