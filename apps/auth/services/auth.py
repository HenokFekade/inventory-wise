from apps.auth.repositories.auth import AuthRepository


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo = repo
