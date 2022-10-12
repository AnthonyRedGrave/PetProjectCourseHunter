from pydantic import BaseModel
from .schemas import User


class LoginResponse(BaseModel):
    accessToken: str
    user: User


class DetailResponse(BaseModel):
    detail: str