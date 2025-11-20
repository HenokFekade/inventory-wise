from typing import List, Dict

from fastapi import HTTPException, status
from starlette.responses import JSONResponse


class UnprocessableEntitiesException(HTTPException):
    _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT

    def __init__(self, errors: Dict[str, List[str]]):
        self.message = "validation error"
        self.names = errors.keys()
        self.messages = errors.values()
        self.errors = errors
        super().__init__(status_code=self._status_code, detail=self.message)

    @classmethod
    def throw(cls, errors: Dict[str, List[str]]):
        raise cls(errors=errors)


def unprocessable_entities_exception_handler(exc: UnprocessableEntitiesException):
    errors: List[Dict[str, List[str]]] = []
    for key, messages in exc.errors.items():
        errors.append({"name": key, "messages": messages})

    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "errors": errors, "status": exc.status_code},
    )
