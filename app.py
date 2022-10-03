from fastapi import FastAPI

from users.models import User
from users.views import users_router
from fastapi.middleware.cors import CORSMiddleware
# from db import init_db

origins = ["*"]


app = FastAPI()
app.include_router(users_router, prefix='/api', tags=['users'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"detail": "HELLO"}
