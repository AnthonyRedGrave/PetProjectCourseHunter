import asyncpg
from psycopg2 import IntegrityError
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from typing import Type, Callable

from db import async_get_db

from fastapi import Depends, Request, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

from repositories import BaseRepository

from users.models import User, Account
from users.schemas import UserLogin
from users.schemas import User as UserBase
from users.security import hash_password, verify_password, sign_jwt, decode_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db=Depends(async_get_db)):
        return Repo_type(db)
    return get_repo


class AdminAPIRepository(BaseRepository):

    async def get_user_by_id(self, user_id: str):
        query = select(User).filter_by(id=int(user_id)).options(selectinload(User.account))
        result = await self.db.execute(query)
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="Not found!")
        return user

    async def delete_user_and_account(self, user: User):
        try:
            await self.db.delete(user.account)
            await self.db.delete(user)
        except sqlalchemy.exc.IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Something went wrong!")

    async def update_user(self, user, user_data):
        try:
            for col in user_data:
                if col[1] is not None:
                    if col[0] == 'account_type':
                        user.account.type = col[1]
                        continue
                    setattr(user, col[0], col[1])
                    await self.db.commit()
        except sqlalchemy.exc.IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Duplicated values!")

    async def async_get_users(self):
        query = select(User).options(selectinload(User.account))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def async_create_user(self, user_in):
        result = await self.db.execute(
            select(User)
            .filter_by(email=user_in.email)
        )
        user = result.scalars().first()
        if user is None:
            try:
                user = User(username=user_in.username,
                            email=user_in.email,
                            hashed_password=hash_password(user_in.password),
                            firstname=user_in.firstname,
                            lastname=user_in.lastname
                            )
            
                account_type = user_in.__dict__.get('account_type', "standart")
                db_user_account = Account(type=account_type, user_id=user.id)
                db_user_account.user = user
                self.db.add_all([user, db_user_account])
                await self.db.commit()

                result = await self.db.execute(
                    select(User)
                    .filter_by(email=user_in.email)
                    .options(selectinload(User.account))
                )
                
                user = result.scalars().first()
                return user
            except SQLAlchemyError:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail="User with this username already exists!")
            
        else:
            raise HTTPException(status_code=400, detail="User with this email already exists!")


async def create_admin_user(db):
    query = select(User).filter_by(email="admin@inbox.ru")
    result = await db.execute(query)
    admin = result.scalars().first()
    if admin is None:
        admin = User(username="admin",
                     email="admin@inbox.ru",
                     hashed_password=hash_password("12345678"),
                     firstname="admin",
                     lastname="adminov"
                     )

        db_user_account = Account(type="admin", user_id=admin.id)
        db_user_account.user = admin
        db.add_all([admin, db_user_account])
        await db.commit()

        return {"detail": "Created!"}
    else:
        return {"detail": "Already exists!"}


def set_cookies_data(resp, response: Response):
    response.set_cookie(key='accessToken', value=resp['accessToken'], httponly=True)


async def get_account_user(db: AsyncSession, user: User):
    query = select(Account).filter_by(user_id=user.id)
    result = await db.execute(query)
    account = result.scalars().first()
    return account


def update_sign_jwt(response, dict):
    return response.update(dict)


async def check_user(db: AsyncSession, data: UserLogin):
    result = await db.execute(
        select(User)
        .filter_by(email=data.email)
        .options(selectinload(User.account))
    )
    user = result.scalars().first()
    if user is None:
        return {"error": "User with this email does not exist!"}

    if not verify_password(data.password, user.hashed_password):
        return {"error": "Wrong password!"}

    response = sign_jwt(user=user, user_account_type=user.account.type.code)

    return response, user


# async def get_current_user(request: Request):
#     credentials: HTTPAuthorizationCredentials = await HTTPBearer().__call__(request)
#     payload = decode_jwt(credentials.credentials)
#     if payload is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth error!")
#
#     return 123