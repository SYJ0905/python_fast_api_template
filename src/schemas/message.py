from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    # create_account: str


class MessageUpdate(BaseModel):
    content: str


class ReplyMessageCreate(BaseModel):
    message_id: str
    content: str
    # create_account: str


class ReplyMessageUpdate(BaseModel):
    content: str
