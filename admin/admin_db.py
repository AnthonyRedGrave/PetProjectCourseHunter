from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from fastapi_core.settings import SYNC_DATABASE_URL

sync_engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True)


def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
    )
    return Session


def get_session():
    Session = create_session()
    try:
        yield Session
    finally:
        Session.remove()
