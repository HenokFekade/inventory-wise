from fastapi import APIRouter, Depends

from apps.auth.controllers.auth import AuthController
from apps.auth.schemas.auth import AdminAuthResponseSchema, AccountLoginSchema
from core.dependencies import auth_controller_dep

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login/account", response_model=AdminAuthResponseSchema)
async def account_login(
        data: AccountLoginSchema,
        controller: AuthController = Depends(auth_controller_dep),
):
    return await controller.account_login(data)

