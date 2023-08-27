from sqlalchemy import Column, String, Integer, ForeignKey
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.model.base import BaseCrud


class User(BaseCrud):
    """
    使用者 Class & Model
    """

    __tablename__ = "user"

    user_id = Column(String(64), primary_key=True)
    username = Column(String(64), unique=True)
    age = Column(Integer)
    email = Column(String(64), unique=True)

    db_session = None

    def __init__(self, db_session: Session, **kwargs):
        super().__init__(db_session)
        self.user_id = kwargs.get("user_id", None)
        self.username = kwargs.get("username", None)
        self.age = kwargs.get("age", None)
        self.email = kwargs.get("email", None)

    def to_dict(self):
        """
        User Response Format
        """

        return {
            "user_id": self.user_id,
            "username": self.username,
            "age": self.age,
            "email": self.email,
        }

    @classmethod
    def set_db_session(cls, db_session: Session):
        """
        設定 db_session
        """

        cls.db_session = db_session

    @staticmethod
    def get_user_list(db_session: Session):
        """
        取得使用者列表
        """

        User.set_db_session(db_session)
        return db_session.query(User).all()

    @staticmethod
    def get_by_user_id(user_id: str, db_session: Session):
        """
        利用 user_id 取得使用者資料
        """

        User.set_db_session(db_session)
        return db_session.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_user_email(email: str, db_session: Session):
        """
        利用 email 取得使用者資料
        """

        User.set_db_session(db_session)
        return db_session.query(User).filter(User.email == email).first()


class Password(BaseCrud):
    """
    使用者密碼 Class & Model
    """

    __tablename__ = "password"

    user_id = Column(
        String(64),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    password_hash = Column(String(128))

    db_session = None

    def __init__(self, db_session: Session, **kwargs):
        super().__init__(db_session)
        self.user_id = kwargs.get("user_id", None)
        self.password_hash = kwargs.get("password_hash", None)

    def set_password(self, password: str):
        """
        設定密碼加密
        """

        self.password_hash = CryptContext(schemes=["bcrypt"]).hash(password)

    def check_password(self, password: str):
        """
        驗證加密密碼
        """

        return CryptContext(schemes=["bcrypt"]).verify(password, self.password_hash)

    @classmethod
    def set_db_session(cls, db_session: Session):
        """
        設定 db_session
        """

        cls.db_session = db_session

    @staticmethod
    def get_by_user_id(user_id: str, db_session: Session):
        """
        利用 user_id 取得使用者資料
        """

        Password.set_db_session(db_session)
        return db_session.query(Password).filter(Password.user_id == user_id).first()
