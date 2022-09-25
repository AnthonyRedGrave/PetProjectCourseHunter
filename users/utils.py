from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.models import User


async def async_get_users(db: AsyncSession):
    query = select(User)
    result = await db.execute(query)
    return result.scalars().all()


async def async_create_user(db: AsyncSession, user_in):
    db_user = User(username=user_in.username,
                   email=user_in.email,
                   hashed_password=user_in.password,
                   firstname=user_in.username,
                   lastname=user_in.username
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user