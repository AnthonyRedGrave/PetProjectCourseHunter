import os
from typing import Generator

import asyncio

import pytest

from db import async_get_db, Base

from app import get_application

from httpx import AsyncClient


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True, future=True)

TestAsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def begin_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture()
async def client() -> AsyncClient:
    await begin_engine()

    async with AsyncClient(app=app, base_url="http://localhost:8008") as ac:
        yield ac


async def _get_test_db():
    async with TestAsyncSessionLocal() as db:
        yield db
        await db.commit()


app = get_application()
app.dependency_overrides[async_get_db] = _get_test_db


# @pytest.fixture(autouse=True)
# async def app():
#     """
#     Create a fresh database on each test case,
#     using async context manager with engine begin
#     """
#     await init_models()
#     # yield app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
