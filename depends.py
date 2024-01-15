from fastapi.security import OAuth2PasswordBearer

oath_scheme = OAuth2PasswordBearer(tokenUrl='/login')