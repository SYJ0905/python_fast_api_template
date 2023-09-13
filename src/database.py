import redis
import rq
from rq import Queue
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import app_env, app_config

SQLALCHEMY_DATABASE_URL = app_config[app_env].SQLALCHEMY_DATABASE_URL

# 创建连接池，SQLAlchemy 默认会使用连接池
engine = create_engine(url=SQLALCHEMY_DATABASE_URL,
                       pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client = redis.Redis(
    host=app_config[app_env].REDIS_HOST, port=app_config[app_env].REDIS_PORT, db=0)
# 創建 Redis 佇列
queue = Queue(connection=redis_client)


# def test_task():
#     print("測試任務已執行")


# # 使用佇列執行測試任務
# queue.enqueue(test_task)


def get_db():
    """
    取得 DB, Transaction
    """

    db_session = SessionLocal()
    print("DataBase 建立連線")
    try:
        yield db_session
    except Exception:
        # 发生异常时回滚事务
        db_session.rollback()
        raise
    finally:
        db_session.close()
        print("DataBase 斷開連線")
