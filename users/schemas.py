from pydantic import BaseModel, validator, ValidationError, constr


class UserRegister(BaseModel):
    username: str
    email: str
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValidationError("passwords are not similar!")
        return v