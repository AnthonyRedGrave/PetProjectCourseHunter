from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    Body,
    status,
)
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder

from pydantic import ValidationError

from fastapi_core.courses.schemas import (
    CategoryDetail,
    Course,
    CourseCreate,
    Category,
    CategoryCreate,
    CourseLesson,
    CourseLessonCreate,
    CourseUpdate,
    DifficultTypeChoices,
)
from fastapi_core.courses.utils import (
    CourseAPIRepository,
    async_create_category,
    async_get_categories,
    async_get_category,
)

from fastapi_core.users.security import JWTBearer
from fastapi_core.users.utils import get_current_user

from fastapi_core.repositories import get_repository
from fastapi_core.db import async_get_db
from fastapi_core.settings import HOST_NAME, MEDIA_PATH
from fastapi_core.utils import upload_file

from sqlalchemy.ext.asyncio.session import AsyncSession

from typing import List, Optional, Union


courses_router = APIRouter()


@courses_router.get("/courses", response_model=list[Course])
async def get_courses(
    # rating: str = None,
    # study_hours: str = None,
    # language: str = None,
    # price: str = None,
    request: Request,
    category: str = None,
    title: str = None,
    course_repo=Depends(get_repository(CourseAPIRepository)),
) -> List[Course]:

    query = await course_repo.get_query()

    q_params = dict(request.query_params)

    return await course_repo.async_filter_courses(query, q_params)


@courses_router.post("/courses", response_model=Course)
async def post_course(
    course_in: CourseCreate,
    course_repo=Depends(get_repository(CourseAPIRepository)),
    current_user=Depends(get_current_user),
) -> Course:
    course = await course_repo.async_create_course(
        course_data=course_in, current_user=current_user
    )
    return course


@courses_router.get("/courses/{course_id}/", response_model=Course)
async def get_course(
    course_id: int, course_repo=Depends(get_repository(CourseAPIRepository))
) -> Course:
    course = await course_repo.async_get_course(course_id=course_id)
    return course


@courses_router.patch("/courses/{course_id}/", response_model=Course)
async def patch_course(
    course_id: int,
    course_in: Optional[CourseUpdate],
    course_repo=Depends(get_repository(CourseAPIRepository)),
    current_user=Depends(get_current_user),
) -> Course:

    course = await course_repo.async_get_course(course_id=course_id)
    if course.publisher != current_user:
        return course

    if course_in is not None:
        await course_repo.async_update_course(course=course, course_in=course_in)

    return course


@courses_router.patch("/courses/{course_id}/upload_video", response_model=Course)
async def upload_course_video(
    course_id: int,
    video: Optional[UploadFile] = File(...),
    current_user=Depends(get_current_user),
    course_repo=Depends(get_repository(CourseAPIRepository)),
):

    course = await course_repo.async_get_course(course_id=course_id)

    if course.publisher != current_user:
        return course

    path = f"{MEDIA_PATH}/courses/{course_id}"
    out_video_name = await upload_file(
        path=path, filename=video.filename, in_file=video
    )
    course.video = f"{HOST_NAME}courses/{course_id}/{out_video_name}"

    return course


@courses_router.patch("/courses/{course_id}/upload_logo", response_model=Course)
async def upload_course_logo(
    course_id: int,
    file: Optional[UploadFile] = File(...),
    current_user=Depends(get_current_user),
    course_repo=Depends(get_repository(CourseAPIRepository)),
):

    course = await course_repo.async_get_course(course_id=course_id)

    if course.publisher != current_user:
        return course

    path = f"{MEDIA_PATH}/courses/{course_id}"
    out_file_name = await upload_file(path=path, filename=file.filename, in_file=file)
    course.preview = f"{HOST_NAME}courses/{course_id}/{out_file_name}"

    return course


@courses_router.get("/courses/{course_id}/video/")
async def get_course_video(
    course_id: int,
    request: Request,
    course_repo=Depends(get_repository(CourseAPIRepository)),
):
    course = await course_repo.async_get_course(course_id=course_id)

    file, status_code, content_length, headers = await course_repo.open_file(
        request, course.video
    )

    response = StreamingResponse(file, media_type="video/mp4", status_code=status_code)

    response.headers.update(
        {"Accept-Ranges": "bytes", "Content-Length": str(content_length), **headers}
    )

    return response


@courses_router.get("/courses/{course_id}/lessons", response_model=Course)
async def get_course_lessons(
    course_id: int,
    course_repo = Depends(get_repository(CourseAPIRepository))
):
    course = await course_repo.async_get_course(course_id = course_id)

    print(course.course_lessons)

    return course

@courses_router.post("/courses/{course_id}/lessons", response_model=Course)
async def post_course_lesson(
    course_id: int,
    lesson_in: CourseLessonCreate,
    course_repo=Depends(get_repository(CourseAPIRepository)),
):
    course = await course_repo.async_get_course(course_id = course_id)

    await course_repo.create_course_lesson(course = course, lesson_in=lesson_in)

    return course




@courses_router.get("/categories", response_model=List[Category])
async def get_categories(db: AsyncSession = Depends(async_get_db)):
    return await async_get_categories(db=db)


@courses_router.get("/categories/{category_id}", response_model=CategoryDetail)
async def get_category(category_id: int, db: AsyncSession = Depends(async_get_db)):
    category = await async_get_category(category_id=category_id, db=db)
    return category



@courses_router.post(
    "/categories", response_model=Category, dependencies=[Depends(JWTBearer())]
)
async def post_category(
    category_in: CategoryCreate, db: AsyncSession = Depends(async_get_db)
):
    category = await async_create_category(db=db, category_data=category_in)
    return category


@courses_router.post(
    "/courses/{course_id}/favorite/", dependencies=[Depends(JWTBearer())]
)
async def favorite_course(
    course_id: int,
    current_user=Depends(get_current_user),
    course_repo=Depends(get_repository(CourseAPIRepository)),
):
    course = await course_repo.async_get_course(course_id=course_id)

    detail = await course_repo.async_favorite_course(course=course, user=current_user)

    return detail


@courses_router.get("/favorites", response_model=List[Course])
async def get_favorites(
    current_user=Depends(get_current_user),
    course_repo=Depends(get_repository(CourseAPIRepository)),
):
    favorites = await course_repo.async_get_favorites(user=current_user)

    return [favorite.course for favorite in favorites]
