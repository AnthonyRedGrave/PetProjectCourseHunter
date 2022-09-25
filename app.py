from fastapi import FastAPI

from users.models import User
from users.views import users_router
# from db import init_db

app = FastAPI()
app.include_router(users_router, prefix='/api', tags=['users'])


# CORSHEADERS FOR FRONTEND
origins = [

]


@app.get("/")
async def main():
    return 123