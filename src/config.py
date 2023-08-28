import os
from pydantic_settings import BaseSettings

app_env = "production"


class Config(BaseSettings):
    """
    Base configuration class for the application.

    This class defines the basic configuration settings for the application.
    It includes settings for the database URL.
    """

    SQLALCHEMY_DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "MESSAGE_BOARD")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class TestingConfig(Config):
    """
    Configuration class for testing environment.

    This class inherits from the base `Config` class and can be used to
    configure settings specific to the testing environment.
    """


class DevelopConfig(Config):
    """
    Configuration class for development environment.

    This class inherits from the base `Config` class and overrides the
    database URL setting for the development environment.
    """

    SQLALCHEMY_DATABASE_URL: str = (
        "mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
    )


class ProductionConfig(Config):
    """
    Configuration class for production environment.

    This class inherits from the base `Config` class and can be used to
    configure settings specific to the production environment.
    """


app_config = {
    "testing": TestingConfig(),
    "develop": DevelopConfig(),
    "production": ProductionConfig(),
}
