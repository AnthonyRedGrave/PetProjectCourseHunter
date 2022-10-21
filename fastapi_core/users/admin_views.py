from typing import List
from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi_core.db import async_get_db
from fastapi_core.repositories import get_repository

from fastapi_core.users.utils import AdminAPIRepository, get_current_user, check_user, create_admin_user
from fastapi_core.users.schemas import UserRegister, UserLogin, User, UserRegisterAccountType, UserUpdate
from fastapi_core.users.security import JWTBearer, sign_jwt
from fastapi_core.users.utils import set_cookies_data
from fastapi_core.users.responses import LoginResponse, DetailResponse


admin_router = APIRouter(prefix="/admin",
                         tags=['admin'],
                         dependencies=[Depends(JWTBearer(permission_type='admin'))])


@admin_router.get("/users/",
                  response_model=List[User])
async def get_users(admin_repo = Depends(get_repository(AdminAPIRepository))) -> List[User]:
    users = await admin_repo.async_get_users()
    return users


@admin_router.post("/users/",
                   status_code=201,
                   response_model=DetailResponse)
async def create_user(user_in: UserRegisterAccountType,
                      admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))):
    await admin_repo.async_create_user(user_in=user_in)
    return DetailResponse(detail="User created!")


@admin_router.patch("/{user_id}/",
                    response_model=User,
                    status_code=200)
async def patch_user(user_id: str,
                     user_data: UserUpdate,
                     admin_repo = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.get_user_by_id(user_id=user_id)
    await admin_repo.update_user(user=user, user_data=user_data)
    return user


@admin_router.delete("/{user_id}/",
                     response_model=DetailResponse)
async def delete_user(user_id: str,
                      admin_repo = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.get_user_by_id(user_id=user_id)
    await admin_repo.delete_user_and_account(user)
    return DetailResponse(detail="User deleted!")



@admin_router.post("/", status_code=201)
async def create_admin(db: AsyncSession = Depends(async_get_db)):
    response = await create_admin_user(db=db)
    return response