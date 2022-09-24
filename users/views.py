from fastapi import APIRouter, Depends
from .models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import Session
from db import get_session, init_db

users_router = APIRouter()


@users_router.get("users/", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(username=user.username, email=user.email, id=user.id) for user in users]