from pydantic import BaseModel, field_validator


class PasswordPayload(BaseModel):
    password: str

    @field_validator("password")
    def strong_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if value.isdigit() or value.isalpha():
            raise ValueError("Password must be alphanumeric")
        return value
