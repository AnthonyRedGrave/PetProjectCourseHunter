import os
from pathlib import Path
import shutil
import aiofiles
from fastapi import APIRouter, Depends, File,Response, UploadFile

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi_core.db import async_get_db
from fastapi_core.repositories import get_repository

from fastapi_core.users.utils import AdminAPIRepository, get_current_user, check_user
from fastapi_core.users.schemas import UserRegister, UserLogin, User, UserUpdate, UserChangePassword
from fastapi_core.users.security import sign_jwt
from fastapi_core.users.utils import set_cookies_data, user_change_password
from fastapi_core.users.responses import LoginResponse
from fastapi_core.settings import HOST_NAME



users_router = APIRouter()


@users_router.get("/users/personal/",
                  tags=["users"],
                  response_model=User)
async def user_current_detail(current_user = Depends(get_current_user)):
    return current_user


@users_router.patch("/users/personal/",
                  response_model=User)
async def user_current_update(user_data: UserUpdate, current_user = Depends(get_current_user), admin_repo = Depends(get_repository(AdminAPIRepository))):
    await admin_repo.update_user(user=current_user, user_data=user_data)
    return current_user


@users_router.get("/users/{user_id}/",
                  tags=["users"], 
                  response_model=User)
async def user_detail_by_id(user_id: int, current_user = Depends(get_current_user), admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.get_user_by_id(user_id=user_id)
    return user


@users_router.post("/users/login/", 
                   tags=["users"],
                   response_model=LoginResponse)
async def user_login(user_login: UserLogin, response: Response, db: AsyncSession = Depends(async_get_db)):
    resp, user = await check_user(db=db, data=user_login)
    if not resp.get("error"):
        set_cookies_data(resp, response=response)
    return LoginResponse(accessToken=resp['accessToken'], user=user)


@users_router.patch("/users/change_password/", 
                   tags=["users"],
                   response_model=User)
async def change_password(user_change_password_data: UserChangePassword, current_user = Depends(get_current_user)):
    await user_change_password(current_user, user_change_password_data)
    return current_user


@users_router.post("/users/upload_image/",
                   response_model=User)
async def upload_image(in_file: UploadFile=File(...), current_user = Depends(get_current_user)):
    async with aiofiles.open(f"media/users/{in_file.filename}", 'wb') as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write
    out_file_name = os.path.basename(f"media/users/{in_file.filename}")
    current_user.image = f"{HOST_NAME}{out_file_name}"
    return current_user


@users_router.post("/users/register/", response_model=LoginResponse)
async def user_register(user_in: UserRegister,
                        admin_repo = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.async_create_user(user_in=user_in)
    response = sign_jwt(user)
    return LoginResponse(accessToken=response['accessToken'], user=user)

