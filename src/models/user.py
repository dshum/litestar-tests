from enum import Enum

import bcrypt
from advanced_alchemy import SQLAlchemyAsyncRepository
from advanced_alchemy.base import UUIDAuditBase
from pydantic import SecretStr
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(str, Enum):
    STUDENT = "Student"
    ADMIN = "Admin"


class User(UUIDAuditBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    _password: Mapped[str] = mapped_column("password_hash", String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)

    @hybrid_property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_password: str):
        new_password_hash = bcrypt.hashpw(
            password=new_password.encode(),
            salt=bcrypt.gensalt(rounds=10),
        )
        self._password = new_password_hash.decode()

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=self.password.encode(),
        )


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User
