from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from apps.account.routes.account import account_router
from exceptions.bad_request import BadRequestException, bad_request_exception_handler
from exceptions.not_found import NotFoundException, not_found_exception_handler
from exceptions.unauthenticated import UnauthenticatedException, unauthenticated_exception_handler
from exceptions.unauthorized import UnauthorizedException, unauthorized_exception_handler


# add start app things to be done
@asynccontextmanager
async def lifespan(_: FastAPI):
    yield

# initialize server
app = FastAPI(lifespan=lifespan, title="Inventory Wise API")

@app.get("/health")
def health():
    return {
        "status": 200,
        "message": "Inventory Wise API Server is running successfully",
    }


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(account_router)
app.include_router(v1_router)


# handle exceptions
@app.exception_handler(BadRequestException)
def handle_bad_request_exception(_, exc: BadRequestException):
    return bad_request_exception_handler(exc=exc)


# handle exceptions
@app.exception_handler(UnauthenticatedException)
def handle_unauthenticated_exception(_, exc: UnauthenticatedException):
    return unauthenticated_exception_handler(exc=exc)


# handle exceptions
@app.exception_handler(UnauthorizedException)
def handle_unauthorized_exception(_, exc: UnauthorizedException):
    return unauthorized_exception_handler(exc=exc)


@app.exception_handler(NotFoundException)
def handle_not_found_exception(_, exc: NotFoundException):
    return not_found_exception_handler(exc=exc)
