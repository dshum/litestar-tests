from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from litestar import post, Controller, get, Request, put, Response
from litestar.di import Provide
from litestar.dto import DTOConfig
from litestar.exceptions import ValidationException, NotAuthorizedException

from api.dependencies import provide_user_service
from lib.jwt_auth import jwt_auth
from models import User
from models.user import UserService
from schemas.auth import LoginUserPayload, UpdatePasswordPayload, RegisterUserPayload
from schemas.user import WriteUserPayload


class UserDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"password", "updated_at", "tests", "assigned_tests"})


class AuthController(Controller):
    dependencies = {
        "user_service": Provide(provide_user_service),
    }
    return_dto = UserDTO

    @post("/register")
    async def register(
            self,
            user_service: UserService,
            data: RegisterUserPayload,
    ) -> Response[User]:
        is_email_unique = await user_service.check_unique_email(data.email)
        if not is_email_unique:
            raise ValidationException("Validation failed", extra=[{
                "message": "This email already exists",
                "key": "email"
            }])
        if data.password != data.confirm_password:
            raise ValidationException("Validation failed", extra=[{
                "message": "Passwords should match",
                "key": "confirm_password"
            }])

        password = data.password.get_secret_value()
        data = data.model_dump(exclude={"confirm_password"})
        data.update({"password": password})
        user = await user_service.create(User(**data), auto_commit=True)

        return jwt_auth.login(
            identifier=str(user.id),
            token_extras={"email": user.email},
            response_body=user,
        )

    @post("/login")
    async def login(
            self,
            user_service: UserService,
            data: LoginUserPayload,
    ) -> Response[User]:
        user = await user_service.get_one_or_none(email=data.email)
        if not user:
            raise NotAuthorizedException("Invalid credentials")
        if not user.verify_password(data.password.get_secret_value()):
            raise NotAuthorizedException("Invalid credentials")
        return jwt_auth.login(
            identifier=str(user.id),
            token_extras={"email": user.email},
            response_body=user,
        )

    @get("/user")
    async def get_user(self, request: Request) -> User:
        return request.user

    @put(path="/user")
    async def update_user(
            self,
            request: Request,
            user_service: UserService,
            data: WriteUserPayload,
    ) -> User:
        is_email_unique = await user_service.check_unique_email(data.email, request.user.id)
        if not is_email_unique:
            raise ValidationException("Validation failed", extra=[{
                "message": "This email already exists",
                "key": "email"
            }])
        data = data.model_dump()
        return await user_service.update(User(**data), request.user.id, auto_commit=True)

    @put(path="/password")
    async def update_password(
            self,
            request: Request,
            user_service: UserService,
            data: UpdatePasswordPayload,
    ) -> User:
        current_password = data.current_password.get_secret_value()
        password = data.password.get_secret_value()

        if not request.user.verify_password(current_password):
            raise ValidationException("Validation failed", extra=[{
                "message": "Invalid current password",
                "key": "current_password"
            }])
        if data.password != data.confirm_password:
            raise ValidationException("Validation failed", extra=[{
                "message": "Passwords should match",
                "key": "confirm_password"
            }])

        return await user_service.update(
            User(password=password),
            request.user.id,
            auto_commit=True
        )
