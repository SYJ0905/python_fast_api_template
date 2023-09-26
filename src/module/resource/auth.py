from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.config import app_env, app_config
from src.database import get_db
from src.model.user import User as UserModel
from src.model.user import Password as PasswordModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class LoginData(BaseModel):
    username: str
    password: str


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=app_config[app_env].SECRET_KEY,
        algorithm=app_config[app_env].ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            key=app_config[app_env].SECRET_KEY,
            algorithms=[app_config[app_env].ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UserModel.get_by_user_email(username, db_session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/users/me")
async def read_users_me(current_user=Depends(get_current_active_user)):
    return {
        "code": "1",
        "data": current_user,
        "message": "",
    }


@router.post("/login")
def login_user(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    """
    登入
    """

    if not login_data.username:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="電子郵件不得為空")
    if not login_data.password:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="密碼不得為空")

    email = login_data.username

    user = UserModel.get_by_user_email(email, db_session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="帳號不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_record = PasswordModel.get_by_user_id(user.user_id, db_session)

    if password_record and not password_record.check_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=app_config[app_env].ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token_expires = timedelta(
        minutes=app_config[app_env].ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
