import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = postgresql+asyncpg://CourseHunter:CourseHunter@db:5432/CourseHunter
# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL ="postgresql://oluktutysqpgxp:a80e778388f93fbe96f8bbbbdd135fb510afc5053a65b2d2db914d7bb39f319b@ec2-99-81-16-126.eu-west-1.compute.amazonaws.com:5432/dchto2hd83c309"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()
