from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    account = relationship("Account", back_populates="user", uselist=False)


class Account(Base):
    TYPES = [
        ('admin', 'Admin account'),
        ('standart', 'Standart account'),
        ('premium', 'Premium account')
    ]
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("profiles", uselist=False))
    type = Column(ChoiceType(TYPES))
    #courses
