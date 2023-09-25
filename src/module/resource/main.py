from fastapi import APIRouter
import socket
from src.config import app_env, app_config

router = APIRouter()


@router.get("/")
def hello():
    """
    取得 hostname
    """

    hostname = socket.gethostname()
    config_info = {
        "APP_ENV": app_env,
        "SQLALCHEMY_DATABASE_URL": app_config[app_env].SQLALCHEMY_DATABASE_URL,
        "SECRET_KEY": app_config[app_env].SECRET_KEY,
        "ALGORITHM": app_config[app_env].ALGORITHM,
        "ACCESS_TOKEN_EXPIRE_MINUTES": app_config[app_env].ACCESS_TOKEN_EXPIRE_MINUTES,
        "REDIS_HOST": app_config[app_env].REDIS_HOST,
        "REDIS_PORT": app_config[app_env].REDIS_PORT,
    }

    return {
        "message": f"Hello Container World! My hostname is {hostname}.",
        "config_info": config_info,
    }
