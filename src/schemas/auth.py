from pydantic import EmailStr, SecretStr, model_validator

from schemas import BaseModel


class LoginUserPayload(BaseModel):
    email: EmailStr
    password: SecretStr


class UpdatePasswordPayload(BaseModel):
    current_password: str
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self) -> "UpdatePasswordPayload":
        if self.password != self.confirm_password:
            raise ValueError("passwords should match")
        return self
