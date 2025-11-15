import secrets

from passlib.context import CryptContext


class PasswordHelper:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, value: str) -> str:
        return cls._pwd_context.hash(value)

    @classmethod
    def verify(cls, value: str, hashed: str) -> bool:
        return cls._pwd_context.verify(value, hashed)
