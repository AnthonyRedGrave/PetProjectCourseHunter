from pydantic import BaseModel, validator, ValidationError, constr
from typing import Optional
from fastapi import HTTPException, status
from enum import Enum
from .models import User as UserDB


class AccountTypeChoices(str, Enum):
    standart = "standart"
    premium = "premium"
    admin = "admin"


class Account(BaseModel):
    type: AccountTypeChoices = AccountTypeChoices.standart

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str
    account: Optional[Account]

    class Config:
        orm_mode = True


class UserPost(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str


class UserRegister(UserPost):
    password: constr(min_length=8)


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
