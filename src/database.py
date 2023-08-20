from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MySQL0905@localhost:3306/message_board"

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
