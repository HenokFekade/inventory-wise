from apps.auth.services.auth import AuthService


class AuthController:
    def __init__(self, service: AuthService):
        self._service = service
