import re
from pydantic import BaseModel, validator
from passlib.context import CryptContext

SECRET_KEY = "7cf3b4a0f8c543e45cb100d16582eadc7a24de5f08d5574fe6ce40bd51ecdb2b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@|.)+$', value):
            raise ValueError('Username format invalid')
        return value
    