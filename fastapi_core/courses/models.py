# from sqlmodel import SQLModel, Field
from fastapi_core.base import Base

from sqlalchemy.orm import relationship, backref

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text, null, Table
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property


from fastapi_core.settings import HOST_NAME


from .mixins import Timestamp


association_table = Table(
    "courses_tools",
    Base.metadata,
    Column("courses_id", ForeignKey("courses.id"), primary_key=True),
    Column("tools_id", ForeignKey("tools.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)
    description = Column(Text, nullable=False)

    logo = Column(String(300), default=f'{HOST_NAME}categories/default_category_logo.png')

    # courses = relationship("Course", lazy='joined', backref=backref("category", uselist=False))
    courses = relationship("Course", back_populates="category", uselist=True)


    def __repr__(self):
        return "<%s id=%s>" % (self.title, self.id)

    def __str__(self) -> str:
        return "<%s id=%s>" % (self.title, self.id)


class CourseTool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)

    courses = relationship("Course", secondary=association_table, back_populates="tools", uselist=True)

    def __repr__(self):
        return "<%s id=%s>" % (self.title, self.id)


class Course(Timestamp, Base):
    DIFFICULTES = [
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard')
    ]
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    difficult = Column(ChoiceType(DIFFICULTES))

    preview = Column(String(300), default=f'{HOST_NAME}courses/default_course_logo.png')

    video = Column(String(300))

    # TODO:
    # comments = relationship("Comment", back_populates="course")
    # subs

    publisher_id = Column(Integer, ForeignKey("users.id"))
    publisher = relationship("User", lazy='selectin', back_populates="published_courses", uselist=False)

    publisher__username = association_proxy(target_collection='publisher', attr='username')

    rating = Column(Integer, index=True, nullable=True)
    study_hours = Column(String(100), nullable=True)

    # tools = relationship("CourseTool", backref=backref("tools", uselist=True))
    tools = relationship("CourseTool", lazy='subquery', secondary=association_table, back_populates="courses", uselist=True)

    course_lessons = relationship("Lesson", lazy='selectin', backref=backref("courses", uselist=True))

    favorites = relationship("CourseFavorite", back_populates="course", lazy='subquery', uselist=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", lazy='selectin', back_populates="courses", uselist=False)

    category_title = association_proxy(target_collection='category', attr='title')

    draft = Column(Boolean, default=True)

    def __repr__(self):
        return "<%s id=%s>" % (self.title, self.id)


class LessonTest(Base):
    __tablename__ = "lesson_tests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)
    
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", back_populates="test")



class LessonAttachment(Base):
    __tablename__ = "lesson_attachments"

    id = Column(Integer, primary_key=True, index=True)

    file = Column(String(300))

    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", back_populates="attachments")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    lesson_time = Column(String(100), nullable=True)
    difficult = Column(Integer)

    test = relationship("LessonTest", back_populates="lesson")

    attachments = relationship("LessonAttachment", back_populates="lesson", uselist=False)

    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", backref=backref("lessons", uselist=False))



class CourseFavorite(Base):
    __tablename__ = "course_favorites"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", lazy='selectin', back_populates="favorites", uselist=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", lazy='selectin', back_populates="favorites", uselist=False)

    active = Column(Boolean, default=True)

    # TODO:
    # comments = 

    # files
    # videos
    


# class CourseSub(Base):
#     subscriber
#     course
#     date_sub
#     status

# Сущность CourseCategory
# название
# курсы
# Описание


# Сущность LESSONTEST
# название

# Сущность COURSE
# название
# описание
# сложность
# комментарии
# те кто подписался на курс
# рейтинг
# время в часах
# инструменты
# автор курса
# дата выхода курса
# Категория (модель)



# Сущность LESSON
# название
# текст описания урока
# время на урок берется из видео
# сложность урока
# комментарии урока
# прикрепляемые файлы
# прикрепляемые видео
# прикрепляемые тесты
# 

# Сущность COURSESUB
# юзер
# курс
# дата подписки
# статус