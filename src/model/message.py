from sqlalchemy import Column, String, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, Session
from src.model.base import BaseCrud


class Message(BaseCrud):
    """
    留言 Class & Model
    """

    __tablename__ = "message"

    message_id = Column(String(36), primary_key=True)
    content = Column(String(200), nullable=False)
    create_account = Column(String(64))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    replies = relationship(
        "Reply", back_populates="message", cascade="all, delete-orphan"
    )

    db_session = None

    def __init__(self, db_session: Session, **kwargs):
        super().__init__(db_session)
        self.message_id = kwargs.get("message_id", None)
        self.content = kwargs.get("content", None)
        self.create_account = kwargs.get("create_account", None)
        self.create_at = kwargs.get("create_at", None)
        self.replies = kwargs.get("replies", [])

    def to_dict(self):
        """
        Message Response Format
        """

        return {
            "message_id": self.message_id,
            "content": self.content,
            "create_account": self.create_account,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "replies": [reply.to_dict() for reply in self.replies],
        }

    @classmethod
    def set_db_session(cls, db_session: Session):
        """
        設定 db_session
        """

        cls.db_session = db_session

    @staticmethod
    def get_message_list(db_session: Session):
        """
        取得留言列表
        """

        Message.set_db_session(db_session)
        return db_session.query(Message).all()

    @staticmethod
    def get_by_message_id(message_id: str, db_session: Session):
        """
        取得單一留言內容
        """

        Message.set_db_session(db_session)
        return (
            db_session.query(Message).filter(
                Message.message_id == message_id).first()
        )


class Reply(BaseCrud):
    """
    留言回覆 Class & Model
    """

    __tablename__ = "reply"

    reply_id = Column(String(36), primary_key=True)
    content = Column(String(200), nullable=False)
    create_account = Column(String(64))
    create_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    message_id = Column(
        String(36), ForeignKey("message.message_id", ondelete="CASCADE")
    )
    message = relationship("Message", back_populates="replies")

    db_session = None

    def __init__(self, db_session: Session, **kwargs):
        super().__init__(db_session)
        self.reply_id = kwargs.get("reply_id", None)
        self.content = kwargs.get("content", None)
        self.create_account = kwargs.get("create_account", None)
        self.create_at = kwargs.get("create_at", None)
        self.message_id = kwargs.get("message_id", None)
        self.message = kwargs.get("message", None)

    def to_dict(self):
        """
        Reply Response Format
        """

        return {
            "reply_id": self.reply_id,
            "content": self.content,
            "create_account": self.create_account,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": self.message_id,
        }

    @classmethod
    def set_db_session(cls, db_session: Session):
        """
        設定 db_session
        """

        cls.db_session = db_session

    @staticmethod
    def get_reply_list_by_message_id(message_id: str, db_session: Session):
        """
        根據留言 id 取得回覆內容
        """

        Reply.set_db_session(db_session)
        message = Message.get_by_message_id(message_id, db_session)
        return message.replies

    @staticmethod
    def get_by_reply_id(reply_id: str, db_session: Session):
        """
        取得單一回覆內容
        """
        Reply.set_db_session(db_session)
        return db_session.query(Reply).filter(Reply.reply_id == reply_id).first()
