import os
from pydantic_settings import BaseSettings

# from datetime import timedelta


class Config(BaseSettings):
    """
    Base configuration class for the application.

    This class defines the basic configuration settings for the application.
    It includes settings for the database URL.
    """

    SQLALCHEMY_DATABASE_URL: str | None = os.environ.get("DATABASE_URL")
    # JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "MESSAGE_BOARD")
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


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
