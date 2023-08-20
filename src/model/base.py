from sqlalchemy.orm import Session
from src.database import Base


class BaseCrud(Base):
    """
    DB CRUD Class
    """

    __abstract__ = True

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self):
        """
        新增資料
        """

        self.db_session.add(self)
        self.db_session.commit()

    def update(self):
        """
        更新&編輯資料
        """

        self.db_session.commit()

    def delete(self):
        """
        刪除資料
        """

        self.db_session.delete(self)
        self.db_session.commit()
