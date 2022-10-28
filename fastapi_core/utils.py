import aiofiles
import os

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import Depends

from fastapi_core.db import async_get_db

from fastapi_core.users.models import User, Account
from fastapi_core.courses.models import Course, Category, CourseTool
from fastapi_core.users.security import hash_password




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
    
    # admin user

    admin = User(username="admin",
                email="admin@inbox.ru",
                hashed_password=hash_password("12345678"),
                firstname="admin_firstname",
                lastname="admin_lastname"
            )
            
    db_admin_account = Account(type="admin", user_id=admin.id)
    db_admin_account.user = admin
    db.add_all([admin, db_admin_account])
    await db.commit()

    # standart user

    user = User(username="sasha",
                email="sasha@inbox.ru",
                hashed_password=hash_password("12345678"),
                firstname="Александр",
                lastname="Трубочкин"
            )
            
    db_user_account = Account(type="standart", user_id=user.id)
    db_user_account.user = user
    db.add_all([user, db_user_account])
    await db.commit()

    # tools

    tools = []

    for tool_title in ['Javascript', 'npm', 'Visual Studio', 'Python', 'Django', 'pip', 'Photoshop', 'Figma']:

        tool = CourseTool(title = tool_title)

        db.add(tool)
        await db.commit
        tools.append(tool)

    # categories

    categories = []

    for category_tuple in [('Frontend', 'Фронт-енд (Frontend) разработчики отвечают за весь цикл разработки передней части\
                     (та, которую мы видим) сайта или приложения (например SPA). Основой Fronted является три компонента. HTML, CSS, JavaScript. Если с первыми двумя все понятно и просто,\
                     то JavaScript открывает огромный "мир" для разработчика с кучей фреймворков вроде Angular, React, Vue и других. Javascript - один из самых востребованых навыков сегодня\
                      в веб-разработке, рекомендуем внимательно ознакомится с ним перед тем, как приступать к изучению фреймворков, или на худой конец глятьте в сторону jquery, который как бы\
                     не хоронили продвинутые разработчики, все же остается подходящим для использование в большинстве проектов. Также Frontend разработчик может работать с различными популярными\
                     cms, вроде Wordpress, Joomla, Opencart.'),

                    ('Backend', 'Backend отвечает за серверную сторону веб-сайта / приложения. Тут, как и в фронт-енде, также есть куда развернутся. Самым популярным языком бек-енда уже много лет\
                     является PHP, несмотря на скептицизм продвинутых программистов, которые хоронят его чуть не каждый год.'), 

                    ('Graphic', 'Работа с графикой. Adobe Photoshop, Lightroom, Illustrator, а также UX/UI дизайн.')]:

        category = Category(title = category_tuple[0],
                            description = category_tuple[1])
        
        db.add(category)
        await db.commit(category)

        categories.append(category)

    # courses

    courses_info = [("React Курс", "Курс по реакту", "easy", 0, (0, 3)), 
                    ("Django Курс", "Курс по Джанго", "medium", 1, (3, 6)), 
                    ("Design Курс", "Курс по дизайну", "hard", 2, (6, -1))]

    for course_info in courses_info:
        
        course = Course(
                title=course_info[0],
                description=course_info[1],
                difficult=course_info[2],
                category = categories[course_info[3]],
                tools = tools[course_info[4][0]:course_info[4][1]]
        )

        db.add(course)


    # django_course = Course(
    #         title="Django Курс",
    #         description="Курс по Джанго",
    #         difficult="medium",
    #         category = categories[1],
    #         tools = tools[3:6]
    # )

    # design_course = Course(
    #         title="Design Курс",
    #         description="Курс по дизайну",
    #         difficult="hard",
    #         category = categories[2],
    #         tools = tools[6:]
    # )
        
    # db.add_all([react_course, django_course, design_course])
        await db.commit()