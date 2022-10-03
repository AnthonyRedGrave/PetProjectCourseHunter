from pydantic import BaseModel, validator, ValidationError, constr
from typing import Optional
from fastapi import HTTPException, status
from enum import Enum
from .models import User as UserDB


class Account(BaseModel):
    type: str


class User(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    account_type: Optional[str] = None

    def __init__(self, user_db: UserDB, **kwargs):
        user_data = user_db.__dict__
        user_account = user_data.pop("account")
        super().__init__(account_type=user_account.type.code, **user_data)

    class Config:
        orm_mode = True


class UserPost(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str


class UserRegister(UserPost):
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            # raise ValidationError("passwords are not similar!")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords are not similar!")
        return v


class AccountTypeChoices(str, Enum):
    standart = "standart"
    premium = "premium"
    admin = "admin"


class UserRegisterAccountType(UserRegister):
    account_type: AccountTypeChoices = AccountTypeChoices.standart


class UserUpdate(UserPost):
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    account_type: AccountTypeChoices = AccountTypeChoices.standart


class UserLogin(BaseModel):
    email: str
    password: constr(min_length=8)
