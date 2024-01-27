from uuid import UUID

from litestar import post, Controller, get, Request, put
from litestar.di import Provide
from litestar.exceptions import NotAuthorizedException
from litestar.params import Parameter

from api.dependencies import provide_user_repo, provide_auth_service
from lib.jwt_auth import jwt_auth
from models.user import UserRepository
from schemas.user import ReadUser, LoginUser, WriteUser, UpdatePassword
from services.auth import AuthService
from services.user import UserService


class AuthController(Controller):
    dependencies = {
        "auth_service": Provide(provide_auth_service),
        "user_repo": Provide(provide_user_repo),
    }

    @post("/login")
    async def login(self, auth_service: AuthService, data: LoginUser) -> ReadUser:
        return await auth_service.login(data)

    @get("/user")
    async def get_user(self, request: Request) -> ReadUser:
        return ReadUser.model_validate(request.user)

    @put(path="/user")
    async def update_user(
            self,
            request: Request,
            auth_service: AuthService,
            data: WriteUser,
    ) -> ReadUser:
        return await auth_service.update_user(data, request.user.id)

    @put(path="/password")
    async def update_password(
            self,
            request: Request,
            auth_service: AuthService,
            data: UpdatePassword,
    ) -> ReadUser:
        return await auth_service.update_password(data, request.user)
