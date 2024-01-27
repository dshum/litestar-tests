from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, SecretStr, field_validator, model_validator
from pydantic_core import PydanticCustomError

from models.user import UserRole
from schemas import BaseModel


class ReadUser(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime


class WriteUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value: str):
        return value.title()

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: str):
        return value.title()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr):
        return value.lower()


class LoginUser(BaseModel):
    email: EmailStr
    password: SecretStr


class UpdatePassword(BaseModel):
    current_password: SecretStr
    password: SecretStr
    confirm_password: SecretStr

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UpdatePassword":
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise PydanticCustomError("Qwe", "Passwords do not match")
        return self
