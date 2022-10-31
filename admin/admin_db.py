from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


# SYNC_DATABASE_URL = "postgresql://CourseHunter:CourseHunter@db:5432/CourseHunter"
SYNC_DATABASE_URL = "postgresql://oluktutysqpgxp:a80e778388f93fbe96f8bbbbdd135fb510afc5053a65b2d2db914d7bb39f319b@ec2-99-81-16-126.eu-west-1.compute.amazonaws.com:5432/dchto2hd83c309"


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
