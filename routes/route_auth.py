from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from security.security import UserModel, password_hasher
from auth.auth_user import get_user
from config.database import collection_auth
from auth.auth_user import verify_password, create_jwt_token

router = APIRouter()


@router.post(
        '/auth',
        tags=['authentication'],
        summary = 'Criar usuário',
        response_model = UserModel
)
async def create_user(user: UserModel):
    user_dict = user.model_dump()
    user_dict['password'] = password_hasher.hash(user_dict['password'])
    result = collection_auth.insert_one(user_dict)

    return user



@router.post(
        '/token',
        tags=['authentication'],
        summary = 'Autenticar e obter token',
        response_model = None,
        include_in_schema = False
)
async def login_for_access_token2(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password
    user = await get_user(username)
    if not user or not verify_password(password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    token_data = {'sub': username}
    return {'access_token': create_jwt_token(token_data), 'token_type': 'bearer'}

    
#  = Depends(oauth2_scheme)
# = Depends(get_current_user)