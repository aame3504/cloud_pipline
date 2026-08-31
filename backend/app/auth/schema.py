from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class SignupRequest(BaseModel):
    email: EmailStr

    username: str = Field(
        min_length=2,
        max_length=100,
    )

    password: str = Field(
        min_length=6,
        max_length=100,
    )


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class MessageResponse(BaseModel):
    success: bool
    message: str