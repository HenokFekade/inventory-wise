import sys
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

# Add the project root to Python path
root_dir = Path(__file__).parent.parent  # Adjust based on your actual structure
sys.path.append(str(root_dir))

# Now import your modules
from core.config.config import config
from apps.account.repositories.account import AccountRepository
from apps.account.routes.account import account_router
from apps.account.services.account import AccountService
from apps.account.controllers.account import AccountController
from apps.auth.routes.auth import auth_router
from apps.auth.services.auth import AuthService
from apps.auth.controllers.auth import AuthController
from connections.database import BaseDatabase
from exceptions.bad_request import BadRequestException, bad_request_exception_handler
from exceptions.not_found import NotFoundException, not_found_exception_handler
from exceptions.unauthenticated import UnauthenticatedException, unauthenticated_exception_handler
from exceptions.unauthorized import UnauthorizedException, unauthorized_exception_handler
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


@pytest.fixture
async def test_db():
    engine = create_async_engine(config.TEST_DATABASE_URL)
    BaseDatabase.metadata.create_all(engine)
    testing_session_local = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        await db.close()
        BaseDatabase.metadata.drop_all(engine)


@pytest.fixture
def test_account_repo(test_db):
    return AccountRepository(test_db)


@pytest.fixture
def test_account_service(test_account_repo):
    return AccountService(repo=test_account_repo)


@pytest.fixture
def test_account_controller(test_account_service):
    return AccountController(service=test_account_service)


@pytest.fixture
def test_auth_service(test_account_repo):
    return AuthService(account_repo=test_account_repo)


@pytest.fixture
def test_auth_controller(test_auth_service):
    return AuthController(service=test_auth_service)


@asynccontextmanager
async def test_lifespan(_: FastAPI):
    yield


@pytest.fixture
def test_app():
    # Create test app with mock lifespan
    app = FastAPI(lifespan=test_lifespan)
    v1_router = APIRouter(prefix="/api/v1")
    app.include_router(account_router)
    app.include_router(auth_router)

    # handle exceptions
    @app.exception_handler(BadRequestException)
    def handle_bad_request_exception(_, exc: BadRequestException):
        return bad_request_exception_handler(exc=exc)

    @app.exception_handler(NotFoundException)
    def handle_not_found_exception(_, exc: NotFoundException):
        return not_found_exception_handler(exc=exc)

    @app.exception_handler(UnauthorizedException)
    def handle_unauthorized_exception(_, exc: UnauthorizedException):
        return unauthorized_exception_handler(exc=exc)

    @app.exception_handler(UnauthenticatedException)
    def handle_unauthenticated_exception(_, exc: UnauthenticatedException):
        return unauthenticated_exception_handler(exc=exc)

    return app


@pytest.fixture
async def test_client(test_db, test_app):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    test_app.dependency_overrides[get_db] = override_get_db  # type: ignore

    with TestClient(test_app) as client:
        yield client
    test_app.dependency_overrides.clear()  # type: ignore
