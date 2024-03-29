from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from litestar import post, Controller, get, Request, put, Response
from litestar.di import Provide
from litestar.dto import DTOConfig
from litestar.exceptions import ValidationException, NotAuthorizedException, ClientException, NotFoundException
from litestar.params import Parameter

from api.dependencies import provide_user_service, provide_password_reset_service
from lib.jwt import jwt_auth, JWT
from models import User
from models.password_reset import PasswordResetService, PasswordReset
from models.user import UserService
from schemas.auth import LoginUserPayload, UpdatePasswordPayload, RegisterUserPayload, ResetPasswordPayload
from schemas.user import WriteUserPayload


class UserDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"password", "updated_at", "tests", "assigned_tests"})


class AuthController(Controller):
    dependencies = {
        "user_service": Provide(provide_user_service),
        "password_reset_service": Provide(provide_password_reset_service),
    }
    return_dto = UserDTO

    @post("/register")
    async def register(
            self,
            request: Request,
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

        request.app.emit("user_registered", user=user)

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

    @post("/verify-email/{email:str}")
    async def verify_email(
            self,
            request: Request,
            user_service: UserService,
            email: str = Parameter(
                title="User email",
                description="A email to verify",
            ),
    ) -> None:
        user = await user_service.get_one_or_none(email=email)
        if not user:
            raise NotFoundException("User not found")
        request.app.emit("verify_email", user=user)
        return None

    @post("/verify/{token:str}")
    async def verify_user(
            self,
            user_service: UserService,
            token: str = Parameter(
                title="JWT Token",
                description="A user token to verify",
            ),
    ) -> Response[User]:
        token = JWT.decode_token(token)
        user = await user_service.get_one_or_none(id=token.sub)
        if not user:
            raise NotFoundException("User not found")
        if user.is_verified:
            raise ClientException("User is already verified")
        user = await user_service.update(User(is_verified=True), user.id, auto_commit=True)
        return jwt_auth.login(
            identifier=str(user.id),
            token_extras={"email": user.email},
            response_body=user,
        )

    @post("/reset-password", return_dto=None)
    async def password_reset(
            self,
            request: Request,
            user_service: UserService,
            password_reset_service: PasswordResetService,
            data: ResetPasswordPayload,
    ) -> None:
        user = await user_service.get_one_or_none(email=data.email)
        if not user:
            raise NotFoundException("User not found")

        data = data.model_dump()
        await password_reset_service.upsert(data=data, item_id=None, match_fields=["email"])
        token = PasswordReset.create_token()
        # password_reset = await password_reset_service.get_one_or_none(email=user.email)
        # if password_reset:
        #     data = data.model_dump()
        #     await password_reset_service.upsert(item_id="email", data=data)
        #
        # await password_reset_service.create(PasswordReset(email=user.email, token=token), auto_commit=True)
        request.app.emit("password_reset", user=user, token=token)
        return None

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
