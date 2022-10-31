from ormar import Boolean
from pydantic import BaseModel, Field, validator
from enum import Enum

from typing import List, Optional


class DifficultTypeChoices(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class LessonAttachment(BaseModel):
    id: int
    file: str


class Tool(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    title: str
    description: str


class CourseCategory(BaseModel):
    id: int
    title: str
    description: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy

    rating: Optional[str] = None
    study_hours: Optional[str] = None

    preview: str

    publisher__username: str = None

    tools: List[Tool]

    @validator("tools")
    def get_tools_titles(cls, v, values):
        return [tool.title for tool in v]

    class Config:
        orm_mode = True

class Category(CategoryCreate):
    id: int
    logo: str

    class Config:
        orm_mode = True


class CategoryDetail(Category):
    courses: List[CourseCategory]


class CourseLesson(BaseModel):
    id: int
    title: str
    description: str
    lesson_time: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy
    # attachments: List[LessonAttachment] = None

    class Config:
        orm_mode = True


class CourseLessonCreate(BaseModel):
    title: str
    description: str
    lesson_time: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy


class Publisher(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str


class Course(BaseModel):
    id: int
    title: str
    description: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy

    rating: Optional[str] = None
    study_hours: Optional[str] = None

    preview: str

    publisher__username: str = None

    tools: List[Tool]

    category: Category

    video: str = None

    course_lessons: List[CourseLesson]

    @validator("tools")
    def get_tools_titles(cls, v, values):
        return [tool.title for tool in v]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CourseCreate(BaseModel):
    title: str
    description: str

    difficult: DifficultTypeChoices = DifficultTypeChoices.easy

    tools: List[str]

    category: str


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    difficult: Optional[DifficultTypeChoices] = None

    tools: Optional[List[str]] = None

    category: Optional[str] = None
