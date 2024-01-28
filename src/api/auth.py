from litestar import post, Controller, get, Request, put
from litestar.di import Provide
from litestar.exceptions import ValidationException, NotAuthorizedException

from api.dependencies import provide_user_service
from lib.jwt_auth import jwt_auth
from models import User
from models.user import UserService
from schemas.auth import LoginUserPayload, UpdatePasswordPayload
from schemas.user import DetailedUser, WriteUserPayload


class AuthController(Controller):
    dependencies = {
        "user_service": Provide(provide_user_service),
    }

    @post("/login")
    async def login(
            self,
            user_service: UserService,
            data: LoginUserPayload,
    ) -> DetailedUser:
        user = await user_service.get_one_or_none(email=data.email)
        if not user:
            raise NotAuthorizedException("Invalid credentials")
        if not user.verify_password(data.password.get_secret_value()):
            raise NotAuthorizedException("Invalid credentials")
        return jwt_auth.login(
            identifier=str(user.id),
            token_extras={"email": user.email},
            response_body=DetailedUser.model_validate(user),
        )

    @get("/user")
    async def get_user(self, request: Request) -> DetailedUser:
        return DetailedUser.model_validate(request.user)

    @put(path="/user")
    async def update_user(
            self,
            request: Request,
            user_service: UserService,
            data: WriteUserPayload,
    ) -> DetailedUser:
        is_email_unique = await user_service.check_unique_email(data.email, request.user.id)
        if not is_email_unique:
            raise ValidationException("Validation failed", extra=[{
                "message": "This email already exists",
                "key": "email"
            }])
        data = data.model_dump()
        user = await user_service.update_and_log(User(**data), request.user.id)
        return DetailedUser.model_validate(user)

    @put(path="/password")
    async def update_password(
            self,
            request: Request,
            user_service: UserService,
            data: UpdatePasswordPayload,
    ) -> DetailedUser:
        if not request.user.verify_password(data.current_password):
            raise ValidationException("Validation failed", extra=[{
                "message": "Invalid current password",
                "key": "current_password"
            }])
        data = data.model_dump(exclude={"current_password", "confirm_password"})
        user = await user_service.update_and_log(User(**data), request.user.id)
        return DetailedUser.model_validate(user)
