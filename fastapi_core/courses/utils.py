from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, subqueryload
from sqlalchemy.exc import SQLAlchemyError

from fastapi_core.repositories import BaseRepository

from fastapi_core.courses.models import Category, Course, CourseTool


async def async_create_category(db, category_data):
    category = Category(title = category_data.title,
                        description = category_data.description)

    await db.add(category)
    await db.commit()
    return category


async def async_get_categories(db):
    query = select(Category)

    result = await db.execute(query)
    return result.scalars().all()



class CourseAPIRepository(BaseRepository):
    async def async_get_courses(self):
        query = select(Course)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_or_create_tools(self, tool_list):
        tools_db = []
        for tool_title in tool_list:
            query = await self.db.execute(select(CourseTool).filter_by(title=tool_title))
            tool = query.scalars().first()
            if tool is None:
                tool = CourseTool(title = tool_title)
                self.db.add(tool)
                self.db.commit()
            tools_db.append(tool)
        return tools_db
            
    async def get_category(self, category_title):
        query = select(Category).filter_by(title=category_title)
        result = await self.db.execute(query)
        category = result.scalars().first()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found!")
        return category
    
    async def async_create_course(self, course_data, current_user):
        try:
            course = Course(title = course_data.title,
                            description = course_data.description,
                            difficult = course_data.difficult)

            category = await self.get_category(category_title=course_data.category_title)

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
            print(e)
            raise HTTPException(status_code=400, detail="Something wrong, please try again!")
