from typing import IO, Generator
from fastapi import HTTPException
from sqlalchemy.future import select
import sqlalchemy.exc
from sqlalchemy.exc import SQLAlchemyError
from fastapi_core.courses.models import CourseRating, Lesson

from fastapi_core.repositories import BaseRepository

from fastapi_core.courses.models import Category, Course, CourseFavorite, CourseTool
from fastapi_core.settings import MEDIA_PATH

import aiofiles


async def async_create_category(db, category_data):
    category = Category(
        title=category_data.title, description=category_data.description
    )

    await db.add(category)
    await db.commit()
    return category


async def async_get_categories(db):
    query = select(Category)

    result = await db.execute(query)
    return result.scalars().all()


async def async_get_category(category_id, db):
    query = select(Category).filter_by(id=category_id)

    result = await db.execute(query)
    return result.scalars().first()


def ranged(
    file: IO[bytes],
    start: int = 0,
    end: int = None,
    block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, "close"):
        file.close()


class CourseAPIRepository(BaseRepository):
    async def get_query(self):
        return select(Course).filter_by(draft=True).order_by(Course.id)

    async def async_get_courses(self):
        query = select(Course).filter_by(draft=True)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def async_filter_courses(self, query, q_params):

        req_cont_params = ('category_title', 'title')

        for k, v in q_params.items():
            if v is not None:
                
                if k in req_cont_params:
                    query = query.filter(getattr(Course, k).contains(v))
                    continue

                query = query.filter(getattr(Course, k).like(v))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_or_create_tools(self, tool_list):
        tools_db = []
        for tool_title in tool_list:
            query = await self.db.execute(
                select(CourseTool).filter_by(title=tool_title)
            )
            tool = query.scalars().first()
            if tool is None:
                tool = CourseTool(title=tool_title)
                self.db.add(tool)
                await self.db.commit()
            tools_db.append(tool)
        return tools_db

    async def create_course_lesson(self, course, lesson_in):
        course_lesson = Lesson(title=lesson_in.title,
                                     description=lesson_in.description,
                                     lesson_time = lesson_in.lesson_time,
                                     difficult = lesson_in.difficult
                                    )
        course_lesson.course = course
        self.db.add(course_lesson)
        await self.db.commit()

    async def get_category(self, category_title):
        query = select(Category).filter_by(title=category_title)
        result = await self.db.execute(query)
        category = result.scalars().first()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found!")
        return category

    async def async_update_course(self, course, course_in):
        try:
            for col in course_in:
                if col[1] is not None:

                    if col[0] is "category":
                        value = await self.get_category(col[1])
                        course.category = value
                        continue

                    elif col[0] is "tools":
                        value = await self.get_or_create_tools(col[1])
                        course.tools = value
                        continue

                    value = col[1]
                    setattr(course, col[0], value)
            await self.db.commit()
        except sqlalchemy.exc.IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Duplicated values!")

    async def async_get_lesson(self, lesson_id):
        query = select(Lesson).filter_by(id=lesson_id)
        result = await self.db.execute(query)
        lesson = result.scalars().first()
        if lesson is None:
            raise HTTPException(status_code=404, detail="Course lesson not found!")
        return lesson

    async def async_get_course(self, course_id):
        query = select(Course).filter_by(id=course_id)
        result = await self.db.execute(query)
        course = result.scalars().first()
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found!")
        return course

    async def async_create_course(self, course_data, current_user):
        try:
            course = Course(
                title=course_data.title,
                description=course_data.description,
                difficult=course_data.difficult,
                language = course_data.language
            )

            category = await self.get_category(
                category_title=course_data.category
            )

            tools = await self.get_or_create_tools(tool_list=course_data.tools)

            course.tools = tools
            course.category = category
            course.publisher = current_user
            self.db.add(course)
            await self.db.commit()

            query = select(Course).filter_by(id=course.id)

            result = await self.db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=400, detail="Something wrong, please try again!"
            )

    async def open_file(self, request, video):
        media_index = video.index(MEDIA_PATH)
        videoname = video[media_index:]
        file = open(videoname, "rb")

        file_stats = await aiofiles.os.stat(videoname)
        file_size = file_stats.st_size

        content_length = file_size
        status_code = 200

        headers = {}
        content_range = request.headers.get("range")  # с какого байта грузить видео

        if content_range is not None:
            content_range = content_range.strip().lower()
            content_ranges = content_range.split("=")[-1]
            range_start, range_end, *_ = map(
                str.strip, (content_ranges + "-").split("-")
            )

            range_start = max(0, int(range_start)) if range_start else 0
            range_end = (
                min(file_size - 1, int(range_end)) if range_end else file_size - 1
            )
            content_length = (range_end - range_start) + 1
            file = ranged(file, start=range_start, end=range_end + 1)
            status_code = 206
            headers["Content-Range"] = f"bytes {range_start}-{range_end}/{file_size}"

        return file, status_code, content_length, headers

    async def async_favorite_course(self, course, user):
        query = select(CourseFavorite).filter_by(course_id=course.id, user_id=user.id)
        result = await self.db.execute(query)
        course_favorite = result.scalars().first()

        detail = None

        if course_favorite is not None:
            course_favorite.active = not course_favorite.active

            detail = "Favorite changed!"

        else:
            course_favorite = CourseFavorite(course=course, user=user)

            self.db.add(course_favorite)
            await self.db.commit()

            detail = "Favorite created!"

        return detail


    async def async_rate_course(self, course, user, rate):
        query = select(CourseRating).filter_by(course_id = course.id, user_id =user.id)

        result = await self.db.execute(query)
        course_rating = result.scalars().first()

        detail = None
        if course_rating is not None:
            if course_rating.status == rate.status:
                raise HTTPException(status_code=400, detail="You can't rate course by same value!")
            course_rating.status = str(int(course_rating.status.value)*-1)

            detail = "Rating changed!"
        else:
            course_rating = CourseRating(course=course, user=user, status=rate.status.value)

            self.db.add(course_rating)

            detail = "Rating created!"

        course.rating += int(course_rating.status)

        await self.db.commit()
        
        return detail

    async def async_get_favorites(self, user):
        query = select(CourseFavorite).filter_by(user_id=user.id)

        result = await self.db.execute(query)

        course_favorites = result.scalars().all()

        return course_favorites
