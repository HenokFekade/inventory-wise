from fastapi import Depends

from apps.auth.services.auth import AuthService
from apps.auth.controllers.auth import AuthController
from core.dependencies.auth.auth_service import auth_service_dep

def auth_controller_dep(service: AuthService = Depends(auth_service_dep)) -> AuthController:
    return AuthController(service)

