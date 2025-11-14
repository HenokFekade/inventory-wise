from fastapi import HTTPException, status
from starlette.responses import JSONResponse


class BadRequestException(HTTPException):
    _status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str = "Bad Request"):
        self.message = message
        super().__init__(status_code=self._status_code, detail=message)

    @classmethod
    def throw(cls, message: str):
        raise cls(message=message)


def bad_request_exception_handler(exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "errors": [], "status": exc.status_code},
    )
