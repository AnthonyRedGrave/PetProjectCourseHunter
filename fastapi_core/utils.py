from typing import List
import aiofiles
import os
from sqlalchemy import select

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import Depends

from fastapi_core.db import async_get_db
from fastapi_core.repositories import BaseRepository

from fastapi_core.users.models import User, Account
from fastapi_core.courses.models import Course, Category, CourseTool
from fastapi_core.users.security import hash_password


class FakeAPIRepository(BaseRepository):
    admin:User = None
    user:User = None
    tools: List[CourseTool] = []
    categories: List[Category] = []

    async def create_admin_user(self):
        admin = User(username="admin",
                email="admin@inbox.ru",
                hashed_password=hash_password("12345678"),
                firstname="admin_firstname",
                lastname="admin_lastname"
            )
            
        db_admin_account = Account(type="admin", user_id=admin.id)
        db_admin_account.user = admin
        self.db.add_all([admin, db_admin_account])
        await self.db.commit()

        FakeAPIRepository.admin = admin

    async def create_default_user(self):
        user = User(username="sasha",
                email="sasha@inbox.ru",
                hashed_password=hash_password("12345678"),
                firstname="Александр",
                lastname="Трубочкин"
            )
            
        db_user_account = Account(type="standart", user_id=user.id)
        db_user_account.user = user
        self.db.add_all([user, db_user_account])
        await self.db.commit()

        FakeAPIRepository.user = user

    async def create_tools(self):
        for tool_title in ['Javascript', 'npm', 'Visual Studio', 'Python', 'Django', 'pip', 'Photoshop', 'Figma']:

            tool = CourseTool(title = tool_title)

            self.db.add(tool)
            await self.db.commit()
            FakeAPIRepository.tools.append(tool)

    async def create_categories(self):
        for category_tuple in [('Frontend', 'Фронт-енд (Frontend) разработчики отвечают за весь цикл разработки передней части'\
                        '(та, которую мы видим) сайта или приложения (например SPA). Основой Fronted является три компонента. HTML, CSS, JavaScript. Если с первыми двумя все понятно и просто,'\
                        'то JavaScript открывает огромный мир для разработчика с кучей фреймворков вроде Angular, React, Vue и других. Javascript - один из самых востребованых навыков сегодня'\
                        'в веб-разработке, рекомендуем внимательно ознакомится с ним перед тем, как приступать к изучению фреймворков, или на худой конец глятьте в сторону jquery, который как бы'\
                        'не хоронили продвинутые разработчики, все же остается подходящим для использование в большинстве проектов. Также Frontend разработчик может работать с различными популярными'\
                        'cms, вроде Wordpress, Joomla, Opencart.'),

                        ('Backend', 'Backend отвечает за серверную сторону веб-сайта / приложения. Тут, как и в фронт-енде, также есть куда развернутся. Самым популярным языком бек-енда уже много лет'\
                        'является PHP, несмотря на скептицизм продвинутых программистов, которые хоронят его чуть не каждый год.'), 

                        ('Graphic', 'Работа с графикой. Adobe Photoshop, Lightroom, Illustrator, а также UX/UI дизайн.')]:

            category = Category(title = category_tuple[0],
                                description = category_tuple[1])
            
            self.db.add(category)
            await self.db.commit()

            FakeAPIRepository.categories.append(category)

    async def create_courses(self):
        courses_info = [("React Курс", "Курс по реакту", "easy", 0, (0, 3)), 
                    ("Django Курс", "Курс по Джанго", "medium", 1, (3, 6)), 
                    ("Design Курс", "Курс по дизайну", "hard", 2, (6, -1))]

        for course_info in courses_info:
            
            course = Course(
                    title=course_info[0],
                    description=course_info[1],
                    difficult=course_info[2],
                    category = FakeAPIRepository.categories[course_info[3]],
                    tools = FakeAPIRepository.tools[course_info[4][0]:course_info[4][1]]
            )

            course.publisher = FakeAPIRepository.user
            self.db.add(course)
            await self.db.commit()

    async def load_data(self):
        query = (
            select(User).filter_by(username="admin")
        )
        result = await self.db.execute(query)
        user = result.scalars().first()
        if user is None:
            await self.create_admin_user()
            await self.create_default_user()
            await self.create_tools()
            await self.create_categories()
            await self.create_courses()

async def upload_file(path, filename, in_file):
    filename = filename.replace(" ", "")
    try:
        out_file = await aiofiles.open(f"{path}/{filename}", 'wb+')
    except FileNotFoundError:
        os.makedirs(path)
        out_file = await aiofiles.open(f"{path}/{filename}", 'wb+')
    content = await in_file.read()  # async read
    await out_file.write(content)  # async write
    out_file_name = os.path.basename(f"{path}/{filename}")
    return out_file_name


async def load_fake_data(db: AsyncSession):
    pass

    