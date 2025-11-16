from typing import List

from fastapi import HTTPException, status
from starlette.responses import JSONResponse


class UnprocessableEntityException(HTTPException):
    _status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, name: str, messages: List[str]):
        self.message = "validation error"
        self.name = name
        self.messages = messages
        super().__init__(status_code=self._status_code, detail=self.message)

    @classmethod
    def throw(cls, name: str, messages: List[str]):
        raise cls(messages=messages, name=name)


def unprocessable_entity_exception_handler(exc: UnprocessableEntityException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "errors": [{"name": exc.name, "messages": exc.messages}]},
    )
