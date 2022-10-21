import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from fastapi_core.db import async_get_db

from fastapi import Depends, Request, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

from fastapi_core.repositories import BaseRepository

from .models import User, Account
from .schemas import UserLogin
from .security import hash_password, verify_password, sign_jwt, decode_jwt

from fastapi_core.settings import HOST_NAME


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


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
            except SQLAlchemyError as e:
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email does not exist!")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password!")

    response = sign_jwt(user)

    return response, user


async def get_current_user(request: Request, db: AsyncSession = Depends(async_get_db)):

    credentials: HTTPAuthorizationCredentials = await HTTPBearer().__call__(request)
    status_bool, detail = decode_jwt(credentials.credentials)
    if not status_bool:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    result = await db.execute(
        select(User)
        .filter_by(email=detail['user_email'])
        .options(selectinload(User.account))
    )
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=400, detail="User with this email does not exists!")

    return user


async def update_current_user(db, current_user, user_data):
    try:
        for col in user_data:
            if col[1] is not None:
                setattr(current_user, col[0], col[1])
                await db.commit()
    except sqlalchemy.exc.IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Duplicated values!")


async def user_change_password(current_user, user_data):
    current_user.hashed_password = hash_password(user_data.password)

