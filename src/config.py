# from datetime import timedelta
from pydantic_settings import BaseSettings
import os


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL")
    # JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "MESSAGE_BOARD")
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class TestingConfig(Config):
    pass


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = (
        "mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
    )
    pass


class ProductionConfig(Config):
    pass


settings = Config()

app_config = {
    "testing": TestingConfig(),
    "develop": DevelopConfig(),
    "production": ProductionConfig(),
}
