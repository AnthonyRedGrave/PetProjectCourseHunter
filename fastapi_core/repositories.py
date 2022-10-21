from typing import Callable, Type

from fastapi import Depends

from fastapi_core.db import async_get_db


class BaseRepository:
    def __init__(self, db):
        self.db = db

def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db=Depends(async_get_db)):
        return Repo_type(db)
    return get_repo