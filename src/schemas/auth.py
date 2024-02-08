from pydantic import EmailStr, SecretStr

from schemas import BaseModel


class LoginUserPayload(BaseModel):
    email: EmailStr
    password: SecretStr


class UpdatePasswordPayload(BaseModel):
    current_password: SecretStr
    password: SecretStr
    confirm_password: SecretStr
