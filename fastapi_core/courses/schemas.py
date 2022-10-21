from pydantic import BaseModel, Field
from enum import Enum

from typing import List, Optional


class DifficultTypeChoices(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class LessonAttachment(BaseModel):
    id: int
    file: str

class CourseLesson(BaseModel):
    id: int
    title: str
    description: str
    lesson_time: str
    difficult: int
    attachments: List[LessonAttachment] = None

    class Config:
        orm_mode = True


class Tool(BaseModel):
    id: int
    title: str
    
    class Config:
        orm_mode = True


class Publisher(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str


class Course(BaseModel):
    # id: int
    title: str
    description: str
    difficult: DifficultTypeChoices = DifficultTypeChoices.easy

    rating: Optional[str] = None
    study_hours: Optional[str] = None

    publisher__username: str = None

    tools: List[Tool]

    category_title: str = None

    draft: bool = None

    video: str = None

    course_lessons: List[CourseLesson]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CategoryCreate(BaseModel):
    title: str
    description: str


class Category(CategoryCreate):
    id: int

    class Config:
        orm_mode = True


class CourseCreate(BaseModel):
    title: str
    description: str

    difficult: DifficultTypeChoices = DifficultTypeChoices.easy
    
    tools: List[str]

    category_title: str
    

