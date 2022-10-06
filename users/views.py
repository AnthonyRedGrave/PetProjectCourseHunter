from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from db import async_get_db
from .utils import AdminAPIRepository, get_repository, check_user, create_admin_user
from .schemas import UserRegister, UserLogin, User, UserRegisterAccountType, UserUpdate
from .security import JWTBearer, sign_jwt
from typing import List
from .utils import set_cookies_data


users_router = APIRouter()


@users_router.get("/users/",
                  dependencies=[Depends(JWTBearer(permission_type='admin'))])
async def get_users(admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))) -> List[User]:
    users = await admin_repo.async_get_users()
    return [User(user) for user in users]


@users_router.post("/users/login/")
async def user_login(user_login: UserLogin, response: Response, db: AsyncSession = Depends(async_get_db)):
    resp = await check_user(db=db, data=user_login)
    if not resp.get("error"):
        set_cookies_data(resp, response=response)
    return resp


@users_router.post("/users/",
                   dependencies=[Depends(JWTBearer(permission_type='admin'))],
                   status_code=201)
async def create_user(user_in: UserRegisterAccountType,
                      admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))):
    await admin_repo.async_create_user(user_in=user_in)
    return {"detail": "User created!"}


@users_router.patch("/users/{user_id}/",
                    response_model=User,
                    dependencies=[Depends(JWTBearer(permission_type='admin'))],
                    status_code=200)
async def patch_user(user_id: str,
                     user_data: UserUpdate,
                     admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.get_user_by_id(user_id=user_id)
    await admin_repo.update_user(user=user, user_data=user_data)
    return {"detail": "User updated!"}


@users_router.delete("/users/{user_id}/",
                     dependencies=[Depends(JWTBearer(permission_type='admin'))])
async def delete_user(user_id: str,
                      admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.get_user_by_id(user_id=user_id)
    await admin_repo.delete_user_and_account(user)
    return {"detail": "User deleted!"}


@users_router.post("/users/admin/", status_code=201)
async def create_admin(db: AsyncSession = Depends(async_get_db)):
    response = await create_admin_user(db=db)
    return response


@users_router.post("/users/register/")
async def user_register(user_in: UserRegister,
                        admin_repo: AsyncSession = Depends(get_repository(AdminAPIRepository))):
    user = await admin_repo.async_create_user(user_in=user_in)
    return sign_jwt(user)
