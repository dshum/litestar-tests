from pydantic import EmailStr, field_validator

from schemas import BaseModel


class WriteUserPayload(BaseModel):
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
