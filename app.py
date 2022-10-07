from fastapi import FastAPI

from users.views import users_router
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from db import engine, Base
=======
# from db import init_db
>>>>>>> 135b20564aff5a8ea97d138ed6376d0a93ee535e

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
