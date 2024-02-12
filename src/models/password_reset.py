import bcrypt
from advanced_alchemy import SQLAlchemyAsyncRepository
from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from lib.service import SQLAlchemyAsyncRepositoryLoggedService


class PasswordReset(UUIDAuditBase):
    __tablename__ = "password_resets"

    email: Mapped[str] = mapped_column(String(320), unique=True)
    _token: Mapped[str] = mapped_column("token_hash", String(1024))

    @hybrid_property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, new_token: str):
        new_token_hash = bcrypt.hashpw(
            password=new_token.encode(),
            salt=bcrypt.gensalt(rounds=10),
        )
        self._token = new_token_hash.decode()

    def verify_token(self, token: str) -> bool:
        return bcrypt.checkpw(
            password=token.encode(),
            hashed_password=self.token.encode(),
        )


class PasswordResetRepository(SQLAlchemyAsyncRepository[PasswordReset]):
    model_type = PasswordReset


# class PasswordResetService(SQLAlchemyAsyncRepositoryLoggedService[PasswordReset]):
#     repository_type = PasswordResetRepository
#
#     async def create(self):

