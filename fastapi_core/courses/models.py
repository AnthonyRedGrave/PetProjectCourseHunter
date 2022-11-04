# from sqlmodel import SQLModel, Field
from fastapi_core.base import Base

from sqlalchemy.orm import relationship, backref

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    Text,
    null,
    Table,
)
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

    logo = Column(
        String(300), default=f"{HOST_NAME}categories/default_category_logo.png"
    )
    courses = relationship("Course", lazy="subquery", back_populates="category", uselist=True)

    def __repr__(self):
        return "<%s id=%s>" % (self.title, self.id)

    def __str__(self) -> str:
        return "<%s id=%s>" % (self.title, self.id)


class CourseTool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)

    courses = relationship(
        "Course", secondary=association_table, back_populates="tools", uselist=True
    )

    def __repr__(self):
        return "<%s id=%s>" % (self.title, self.id)


class Course(Timestamp, Base):
    DIFFICULTES = [("easy", "easy"), ("medium", "medium"), ("hard", "hard")]
    LANGUAGES = [("english", "english"), ("russian", "russian")]
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    difficult = Column(ChoiceType(DIFFICULTES))

    preview = Column(String(300), default=f"{HOST_NAME}courses/logo_default.png")

    language = Column(ChoiceType(LANGUAGES))

    video = Column(String(300))

    # TODO:
    # comments = relationship("Comment", back_populates="course")
    # subs

    publisher_id = Column(Integer, ForeignKey("users.id"))
    publisher = relationship(
        "User", lazy="selectin", back_populates="published_courses", uselist=False
    )

    publisher__username = association_proxy(
        target_collection="publisher", attr="username"
    )

    rating = Column(Integer, index=True, default=0)
    study_hours = Column(String(100), nullable=True)

    tools = relationship(
        "CourseTool",
        lazy="subquery",
        secondary=association_table,
        back_populates="courses",
        uselist=True,
    )

    course_lessons = relationship(
        "Lesson", lazy="subquery", back_populates="course", uselist=True, order_by=lambda: Lesson.id,
    )

    favorites = relationship(
        "CourseFavorite", back_populates="course", lazy="subquery", uselist=True
    )

    ratings = relationship(
        "CourseRating", back_populates="course", lazy='subquery', uselist=True
    )

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(
        "Category", lazy="selectin", back_populates="courses", uselist=False
    )

    category_title = association_proxy(target_collection="category", attr="title")

    draft = Column(Boolean, default=True)

    @hybrid_property
    def count_lessons(self):
        return len(self.course_lessons)


    @hybrid_property
    def rated(self):
        rated_dict = {'like': 0, 'dislike': 0}
        likes = [rate.status for rate in self.ratings if int(rate.status.value) > 0]
        rated_dict['like'] = len(likes)
        dislikes = [rate.status for rate in self.ratings if int(rate.status.value) < 0]
        rated_dict['dislike'] = len(dislikes)
        return rated_dict
    

    def __repr__(self):
        return "<%s id=%s>" % (self.title, self.id)


class LessonTest(Base):
    __tablename__ = "lesson_tests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)

    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", back_populates="test")

    questions = relationship("TestQuestion", back_populates="lesson_test", uselist=True)


class LessonAttachment(Base):
    __tablename__ = "lesson_attachments"

    id = Column(Integer, primary_key=True, index=True)

    file = Column(String(300))

    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", back_populates="attachments")


class Lesson(Base):
    DIFFICULTES = [("easy", "easy"), ("medium", "medium"), ("hard", "hard")]
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    lesson_time = Column(String(100), nullable=True)
    difficult = Column(ChoiceType(DIFFICULTES))

    test = relationship("LessonTest", back_populates="lesson")

    attachments = relationship(
        "LessonAttachment", back_populates="lesson", uselist=False
    )

    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(
        "Course", lazy="selectin", back_populates="course_lessons", uselist=False
    )

    video = Column(String(300))

    def __repr__(self):
        return "<Lesson object %s id=%s>" % (self.title, self.id)


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)

    description = Column(Text, nullable=False)

    lesson_test_id = Column(Integer, ForeignKey("lesson_tests.id"))
    lesson_test = relationship("LessonTest", lazy="selectin", back_populates="questions", uselist=False)

    answers = relationship("TestAnswer", back_populates="question", uselist=True)


class TestAnswer(Base):
    __tablename__ = "test_answers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)

    correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey("test_questions.id"))
    question = relationship(
        "TestQuestion", lazy="selectin", back_populates="answers", uselist=False
    )


class CourseRating(Base):
    RATINGS_STATUSES = [
        ("1", "1"),
        ("-1", "-1")
    ]
    __tablename__ = "course_ratings"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(
        "Course", back_populates="ratings", uselist=False
    )

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User", back_populates="ratings", uselist=False
    )

    status = Column(ChoiceType(choices=RATINGS_STATUSES))



class CourseFavorite(Base):
    __tablename__ = "course_favorites"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship(
        "Course", lazy="selectin", back_populates="favorites", uselist=False
    )

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User", lazy="selectin", back_populates="favorites", uselist=False
    )

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
