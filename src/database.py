from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import app_env, app_config

SQLALCHEMY_DATABASE_URL = app_config[app_env].SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    取得 DB
    """

    db_session = SessionLocal()
    print("DataBase 建立連線")
    try:
        yield db_session
    finally:
        print("DataBase 斷開連線")
        db_session.close()
