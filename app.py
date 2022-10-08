from fastapi import FastAPI

from users.views import users_router
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from users.models import User

from sqladmin import Admin, ModelView

origins = ["*"]

class UserAdmin(ModelView, model = User):
    column_list = [User.id, User.username]
    details_template = "details.html"
    list_template = "list.html"


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(users_router, prefix='/api', tags=['users'])
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()

admin = Admin(app, engine, templates_dir="templates")
admin.add_view(UserAdmin)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def main():
    return {"detail": "HELLO"}
