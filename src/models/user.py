from datetime import timedelta, datetime
from enum import Enum
from typing import List, TYPE_CHECKING, Any
from uuid import UUID

import bcrypt
from advanced_alchemy import SQLAlchemyAsyncRepository, ModelT
from advanced_alchemy.base import UUIDAuditBase
from litestar.security.jwt import Token
from sqlalchemy import String, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib import settings
from lib.jwt_auth import jwt_auth
from lib.service import SQLAlchemyAsyncRepositoryLoggedService
from mails.user_registered import UserRegisteredMail

if TYPE_CHECKING:
    from models import UserTest


class UserRole(str, Enum):
    STUDENT = "Student"
    ADMIN = "Admin"


class User(UUIDAuditBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    _password: Mapped[str] = mapped_column("password_hash", String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
    tests: Mapped[List["UserTest"]] = relationship(
        foreign_keys="UserTest.user_id",
        back_populates="user",
        lazy="noload",
    )
    assigned_tests: Mapped[List["UserTest"]] = relationship(
        foreign_keys="UserTest.creator_user_id",
        back_populates="creator_user",
        lazy="noload",
    )

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

    @property
    def name(self) -> bool:
        return self.first_name + " " + self.last_name

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=self.password.encode(),
        )


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User


class UserService(SQLAlchemyAsyncRepositoryLoggedService[User]):
    repository_type = UserRepository

    async def check_unique_email(self, email: str, user_id: UUID | None = None) -> bool:
        statement = select(User).where(User.email == email)
        if user_id:
            statement = statement.where(User.id != user_id)
        user_count = await self.count(statement=statement)
        return user_count < 1

    async def register(self, data: ModelT | dict[str, Any], **kwargs: Any) -> ModelT:
        user = await super().create(data, auto_commit=True)
        await UserRegisteredMail(user=user).send()
        return user
