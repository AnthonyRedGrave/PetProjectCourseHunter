from fastapi import FastAPI

from .users.views import users_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from .db import engine
from .users.models import Base


origins = ["*"]


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

# @flask_app.route("/")
# def flask_admin():
#     return {"HELLO": "FLASK"}



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
