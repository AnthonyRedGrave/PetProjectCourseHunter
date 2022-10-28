import pytest
from users.schemas import UserRegister
import json


# тест создание админа
# тест просмотр юзеров
# тест редактирование юзера
# тест удаление юзера
# тест создание юзера админом

pytestmark = pytest.mark.asyncio


# async def test_create_admin__success(client):
#     response = await client.post("/api/users/admin")
#     assert response.json() == {'detail': 'Created!'}


async def test_get_users__success(client):

    response = await client.post("/api/users/admin")
    assert response.json() == {"detail": "Created!"}

    user_data = {"email": "admin@inbox.ru", "password": "12345678"}
    response = await client.post("/api/users/login", data=json.dumps(user_data))

    auth_data = {"scheme": "Bearer", "credentials": response.json()["accessToken"]}

    response = await client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {response.json()['accessToken']}"},
    )
    print(response.json())
    assert response.json() == []


# async def test_get_users__error(client):
#     pass


# async def test_user_login__error(client):
#
#     user_data = {
#         "email": "admin@inbox.ru",
#         "password": "12345678"
#     }
#     response = await client.post("/api/users/login", data=json.dumps(user_data))
#     assert response.json() == {'error': 'User with this email does not exist!'}
