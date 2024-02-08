from pydantic import EmailStr, SecretStr

from schemas import BaseModel


class RegisterUserPayload(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr


class LoginUserPayload(BaseModel):
    email: EmailStr
    password: SecretStr


class UpdatePasswordPayload(BaseModel):
    current_password: SecretStr
    password: SecretStr
    confirm_password: SecretStr
