import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = postgresql+asyncpg://CourseHunter:CourseHunter@db:5432/CourseHunter
# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgres://lzymozdotgazte:dcd435e4b52bb8ccb1fdf85766c83d870a5488160be3881e30212547aa4c7cc6@ec2-54-228-30-162.eu-west-1.compute.amazonaws.com:5432/d3lotjev0237d1"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()
