from fastapi import APIRouter, Depends

from fastapi_core.courses.schemas import Course, CourseCreate, Category, CategoryCreate
from fastapi_core.courses.utils import CourseAPIRepository, async_create_category, async_get_categories

from fastapi_core.users.security import JWTBearer
from fastapi_core.users.utils import get_current_user

from fastapi_core.repositories import get_repository
from fastapi_core.db import async_get_db

from sqlalchemy.ext.asyncio.session import AsyncSession

from typing import List



courses_router = APIRouter()

@courses_router.get("/courses", response_model=list[Course], dependencies=[Depends(JWTBearer())])
async def get_courses(course_repo = Depends(get_repository(CourseAPIRepository))) -> List[Course]:
    courses = await course_repo.async_get_courses()
    print(courses[0].__dict__)
    return courses


@courses_router.post("/courses", response_model=Course, dependencies=[Depends(JWTBearer())])
async def post_course(course_in: CourseCreate, course_repo = Depends(get_repository(CourseAPIRepository)), current_user = Depends(get_current_user)) -> Course:
    course = await course_repo.async_create_course(course_data = course_in, current_user=current_user)
    print(course.__dict__)
    return course


@courses_router.get("/categories", response_model=List[Category], dependencies=[Depends(JWTBearer())])
async def get_categories(db: AsyncSession = Depends(async_get_db)):
    return await async_get_categories(db=db)


@courses_router.post("/categories", response_model=Category, dependencies=[Depends(JWTBearer())])
async def post_category(category_in: CategoryCreate, db: AsyncSession = Depends(async_get_db)):
    category = await async_create_category(db=db, category_data = category_in)
    return category