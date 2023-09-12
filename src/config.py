import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

app_env = os.environ.get("APP_ENV")


class Config(BaseSettings):
    """
    Base configuration class for the application.

    This class defines the basic configuration settings for the application.
    It includes settings for the database URL.
    """

    SQLALCHEMY_DATABASE_URL: str = os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    )


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


print(f"APP_ENV: {app_env}")
print(f"SQLALCHEMY_DATABASE_URL: {app_config[app_env].SQLALCHEMY_DATABASE_URL}")
print(f"SECRET_KEY: {app_config[app_env].SECRET_KEY}")
print(f"ALGORITHM: {app_config[app_env].ALGORITHM}")
print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {app_config[app_env].ACCESS_TOKEN_EXPIRE_MINUTES}")
