from datetime import datetime
from ormar import Boolean
from pydantic import BaseModel, Field, validator
from enum import Enum

from typing import List, Optional


class RatingTypeChoices(str, Enum):
    incr = "1"
    decr = "-1"


class LanguageTypeChoices(str, Enum):
    english = "english"
    russian = "russian"


class DifficultTypeChoices(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class CourseRate(BaseModel):
    status: RatingTypeChoices


class CourseFilter(BaseModel):
    category_title: Optional[str] = None
    title: Optional[str] = None
    language: Optional[LanguageTypeChoices] = None

    # length: Optional[str] = None
    # rating: Optional[str] = None
    # price: Optional[str] = None


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


class Category(CategoryCreate):
    id: int
    logo: str

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    id: int
    title: str
    description: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy
    language: LanguageTypeChoices = LanguageTypeChoices.russian
    rating: Optional[str] = None
    study_hours: Optional[str] = None
    publisher__username: str = None
    category: Category
    tools: List[Tool]

    rated: dict

    count_lessons: int

    created_at: datetime

    @validator("created_at")
    def parse_created_at(cls, v, values):
        return v.date().strftime("%d/%m/%Y")

    @validator("tools")
    def get_tools_titles(cls, v, values):
        return [tool.title for tool in v]

    class Config:
        orm_mode = True


class CourseLesson(BaseModel):
    id: int
    title: str
    description: str
    lesson_time: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy
    video: str = None
    # attachments: List[LessonAttachment] = None

    class Config:
        orm_mode = True


class CourseDetail(CourseBase):
    video: str = None
    course_lessons: List[CourseLesson]


class Course(CourseBase):
    pass


class CourseCategory(Course):
    pass


class CategoryDetail(Category):
    courses: List[CourseCategory]


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


class CourseCreate(BaseModel):
    title: str
    description: str

    difficult: DifficultTypeChoices = DifficultTypeChoices.easy
    language: LanguageTypeChoices = LanguageTypeChoices.russian

    tools: List[str]

    category: str


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    difficult: Optional[DifficultTypeChoices] = None

    tools: Optional[List[str]] = None

    category: Optional[str] = None
