from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str
    username: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserRegister(UserBase):
    pass
