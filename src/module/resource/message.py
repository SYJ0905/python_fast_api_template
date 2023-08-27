import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.module.resource.auth import get_current_active_user
from src.model.message import Message as MessageModel
from src.model.message import Reply as ReplyModel
from src.schemas.message import (
    MessageCreate,
    MessageUpdate,
    ReplyMessageCreate,
    ReplyMessageUpdate,
)

router = APIRouter()


@router.get("/messages")
def message_list(
    current_user=Depends(get_current_active_user), db_session: Session = Depends(get_db)
):
    """
    取得所有留言列表
    """

    message_list_data = [
        message.to_dict() for message in MessageModel.get_message_list(db_session)
    ]
    return {"code": "1", "data": message_list_data, "message": "查詢所有留言成功"}


@router.post("/message")
def create_message(
    message_data: MessageCreate,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    建立留言
    """

    if not message_data.content:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="留言內容不得為空")
    # if not message_data.create_account:
    #     raise HTTPException(status_code=status.HTTP_200_OK, detail="留言者不得為空")

    message_id = str(uuid.uuid4()).replace("-", "")
    message = MessageModel(
        message_id=message_id,
        content=message_data.content,
        # create_account=get_jwt_identity(),
        db_session=db_session,
    )

    message.add()

    message_list_data = [
        message.to_dict() for message in MessageModel.get_message_list(db_session)
    ]
    return {"code": "1", "data": message_list_data, "message": "新增留言成功"}


@router.put("/message/{message_id}")
def update_message(
    message_id: str,
    message_data: MessageUpdate,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    更新留言
    """

    if not message_data.content:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="留言內容不得為空")
    # if not message_data.create_account:
    #     raise HTTPException(status_code=status.HTTP_200_OK, detail="留言者不得為空")

    message = MessageModel.get_by_message_id(message_id, db_session)

    if not message:
        return {"code": "0", "data": None, "message": "留言不存在"}

    # if message.create_account != get_jwt_identity():
    #   return {"code": "0", "data": None, "message": "拒絕不同帳號更新留言"}

    message.content = message_data.content
    message.update()

    message_list_data = [
        message.to_dict() for message in MessageModel.get_message_list(db_session)
    ]
    return {"code": "1", "data": message_list_data, "message": "更新留言成功"}


@router.delete("/message/{message_id}")
def delete_message(
    message_id: str,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    刪除留言
    """

    message = MessageModel.get_by_message_id(message_id, db_session)

    if not message:
        return {"code": "0", "data": None, "message": "留言不存在"}

    # if message.create_account != get_jwt_identity():
    #     return {"code": "0", "data": None, "message": "拒絕不同帳號刪除留言"}

    message.delete()

    message_list_data = [
        message.to_dict() for message in MessageModel.get_message_list(db_session)
    ]
    return {"code": "1", "data": message_list_data, "message": "刪除留言成功"}


@router.post("/reply")
def create_reply(
    reply_message_data: ReplyMessageCreate,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    建立回覆
    """

    message_id = reply_message_data.message_id

    if not message_id:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="指定留言編號不得為空")

    if not reply_message_data.content:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="回覆內容不得為空")

    message = MessageModel.get_by_message_id(message_id, db_session)

    if not message:
        return {"code": "0", "data": None, "message": "指定的留言不存在"}

    reply = ReplyModel(
        reply_id=str(uuid.uuid4()).replace("-", ""),
        message_id=message_id,
        content=reply_message_data.content,
        # create_account=get_jwt_identity(),
        message=message,
        db_session=db_session,
    )

    reply.add()

    reply_list_data = [
        reply.to_dict()
        for reply in ReplyModel.get_reply_list_by_message_id(message_id, db_session)
    ]
    return {"code": "1", "data": reply_list_data, "message": "新增回覆成功"}


@router.put("/reply/{reply_id}")
def update_reply(
    reply_id: str,
    reply_message_data: ReplyMessageUpdate,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    reply = ReplyModel.get_by_reply_id(reply_id, db_session)

    if not reply:
        return {"code": "0", "data": None, "message": "回覆不存在"}

    if not reply_message_data.content:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="回覆內容不得為空")

    # if reply.create_account != get_jwt_identity():
    #     return {"code": "0", "data": None, "message": "拒絕不同帳號更新回覆"}

    reply.content = reply_message_data.content
    reply.update()

    reply_list_data = [
        reply.to_dict()
        for reply in ReplyModel.get_reply_list_by_message_id(
            reply.message_id, db_session
        )
    ]
    return {"code": "1", "data": reply_list_data, "message": "更新回覆成功"}


@router.delete("/reply/{reply_id}")
def delete_reply(
    reply_id: str,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    reply = ReplyModel.get_by_reply_id(reply_id, db_session)

    if not reply:
        return {"code": "0", "data": None, "message": "回覆不存在"}

    # if reply.create_account != get_jwt_identity():
    #     return {"code": "0", "data": None, "message": "拒絕不同帳號刪除回覆"}

    reply.delete()

    reply_list_data = [
        reply.to_dict()
        for reply in ReplyModel.get_reply_list_by_message_id(
            reply.message_id, db_session
        )
    ]
    return {"code": "1", "data": reply_list_data, "message": "刪除回覆成功"}
