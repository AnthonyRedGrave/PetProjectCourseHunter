from fastapi import FastAPI

from users.views import users_router
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def main():
    return {"detail": "HELLO"}
