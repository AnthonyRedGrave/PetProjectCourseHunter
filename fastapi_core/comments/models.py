from fastapi_core.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship, backref
from fastapi_core.users.models import User
from fastapi_core.courses.models import Course, Lesson



# class AbstractComment(Base):
#     __abstract__ = True
#     id = Column(Integer, primary_key=True, index=True)
#     text = Column(Text, nullable=False)

#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", backref=backref("comments", uselist=False))



# class CourseComment(AbstractComment):
#     __tablename__ = "course_comments"

#     course_id = Column(Integer, ForeignKey("courses.id"))
#     course = relationship("Course", backref=backref("comments", uselist=False))


# class LessonComment(AbstractComment):
#     __tablename__ = "lesson_comments"

#     lesson_id = Column(Integer, ForeignKey("lessons.id"))
#     lesson = relationship("Lesson", backref=backref("comments", uselist=False))