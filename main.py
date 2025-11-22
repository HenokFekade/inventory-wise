from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from apps.account.routes.account import account_router
from apps.file_upload.routes.file_upload import file_upload_router
from apps.file_upload.services.cloudinary_file_upload import CloudinaryFileUploadService
from exceptions.unprocessable_entities import UnprocessableEntitiesException, unprocessable_entities_exception_handler
from apps.auth.routes.auth import auth_router
from apps.category.routes.category import category_router
from apps.color.routes.color import color_router
from apps.currency.routes.currency import currency_router
from apps.customer.routes.customer import customer_router
from apps.item.routes.item import item_router
from apps.size.routes.size import size_router
from apps.store.routes.store import store_router
from apps.store_item.routes.store_item import store_item_router
from apps.supplier.routes.supplier import supplier_router
from apps.tax.routes.tax import tax_router
from apps.unit.routes.unit import unit_router
from exceptions.bad_request import BadRequestException, bad_request_exception_handler
from exceptions.not_found import NotFoundException, not_found_exception_handler
from exceptions.unauthenticated import UnauthenticatedException, unauthenticated_exception_handler
from exceptions.unauthorized import UnauthorizedException, unauthorized_exception_handler
from exceptions.unprocessable_entity import UnprocessableEntityException, unprocessable_entity_exception_handler
from seeder.seed import seed


# add start app things to be done
@asynccontextmanager
async def lifespan(_: FastAPI):
    # seed data
    await seed()
    CloudinaryFileUploadService.initialize()
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
v1_router.include_router(auth_router)
v1_router.include_router(category_router)
v1_router.include_router(color_router)
v1_router.include_router(currency_router)
v1_router.include_router(customer_router)
v1_router.include_router(file_upload_router)
v1_router.include_router(item_router)
v1_router.include_router(size_router)
v1_router.include_router(supplier_router)
v1_router.include_router(store_router)
v1_router.include_router(store_item_router)
v1_router.include_router(tax_router)
v1_router.include_router(unit_router)
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


# handle exceptions
@app.exception_handler(UnprocessableEntityException)
def handle_unprocessable_entity_exception(_, exc: UnprocessableEntityException):
    return unprocessable_entity_exception_handler(exc=exc)


# handle exceptions
@app.exception_handler(UnprocessableEntitiesException)
def handle_unprocessable_entities_exception(_, exc: UnprocessableEntitiesException):
    return unprocessable_entities_exception_handler(exc=exc)
