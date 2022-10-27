from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_core.users.views import users_router
from fastapi_core.courses.views import courses_router
from fastapi_core.users.admin_views import admin_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_core.db import engine
from fastapi_core.base import Base
from fastapi_core.settings import MEDIA_PATH



# script_dir = os.path.dirname(__file__)
# st_abs_file_path = os.path.join(script_dir, "media/")

origins = ["*"]



def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(users_router, prefix='/api', tags=['users'])
    application.include_router(courses_router, prefix='/api', tags=['courses'])
    application.include_router(admin_router)
    application.mount(f"/{MEDIA_PATH}", StaticFiles(directory=f"{MEDIA_PATH}/"), name=MEDIA_PATH)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def main():
    return {"detail": "HELLO"}
