from pydantic import BaseModel, validator, ValidationError, constr
from typing import List, Optional
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


class PublishedCourse(BaseModel):
    id: int
    title: str
    description: str
    rating: Optional[str] = None
    study_hours: Optional[str] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str
    account: Optional[Account]
    image: str
    published_courses: List[PublishedCourse]

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


class UserLogin(BaseModel):
    email: str
    password: constr(min_length=8)


class UserChangePassword(BaseModel):
    password: str
    repeat_password: str

    @validator("repeat_password")
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=403, detail="passwords are not similar!")
        return v