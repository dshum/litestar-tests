from uuid import UUID

from litestar.exceptions import NotAuthorizedException, ValidationException
from pydantic import ValidationError

from lib.jwt_auth import jwt_auth
from models.user import UserRepository, User
from schemas.user import LoginUser, ReadUser, WriteUser, UpdatePassword


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login(self, data: LoginUser) -> ReadUser:
        user = await self.repository.get_one_or_none(email=data.email)
        if not user:
            raise NotAuthorizedException("Invalid credentials")
        if not user.verify_password(data.password.get_secret_value()):
            raise NotAuthorizedException("Invalid credentials")
        return jwt_auth.login(
            identifier=str(user.id),
            token_extras={"email": user.email},
            response_body=ReadUser.model_validate(user),
        )

    async def update_user(self, data: WriteUser, user_id: UUID) -> ReadUser:
        data = data.model_dump()
        data.update({"id": user_id})
        obj = await self.repository.update(User(**data))
        await self.repository.session.commit()
        return ReadUser.model_validate(obj)

    async def update_password(self, data: UpdatePassword, user: User) -> ReadUser:
        if not user.verify_password(data.current_password.get_secret_value()):
            raise ValidationException("Validation failed", extra=[{
                "message": "Invalid current password",
                "key": "current_password"
            }])
        password = data.password.get_secret_value()
        obj = await self.repository.update(User(id=user.id, password=password))
        await self.repository.session.commit()
        return ReadUser.model_validate(obj)
