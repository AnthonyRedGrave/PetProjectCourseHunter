from fastapi import APIRouter, Depends
from .models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from db import async_get_db
from .utils import async_get_users, async_create_user
from .schemas import UserRegister


users_router = APIRouter()


@users_router.get("/users/")
async def get_users(db: AsyncSession = Depends(async_get_db)):
    users = await async_get_users(db=db)
    return users


@users_router.post("/users/")
async def user_register(user_in: UserRegister, db:AsyncSession = Depends(async_get_db)):
    return await async_create_user(db=db, user_in=user_in)
    # return []


# @users_router.post("/users/")
# async def post_users(user_register: UserRegister, sesion: AsyncSession = Depends(get_session)):
#     print(user_register)
#     return 123