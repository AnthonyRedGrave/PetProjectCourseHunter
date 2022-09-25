from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Enum, Text
from db import Base


class User(Base):
    __tablename__ = "users"
    id =  Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)


# class Account(Base):
#     __tablename__ = "profiles"
#     id:
#     user:
#     type:
#     #courses
