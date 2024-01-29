import re
from pydantic import BaseModel, field_validator
from passlib.context import CryptContext


password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@|.)+$', value):
            raise ValueError('Username format invalid')
        return value
