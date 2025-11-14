from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from apps.account.models.account import AccountModel
from core.authentications.token import TokenAuth
from core.dependencies.token import token_dep

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def super_admin_dep(
        token: Annotated[str, Depends(_oauth2_scheme)],
        token_auth: TokenAuth = Depends(token_dep),
) -> AccountModel:
    return await token_auth.super_admin(token)
