import uuid
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.module.resource.auth import get_current_active_user
from src.model.user import User as UserModel
from src.model.user import Password as PasswordModel
from src.schemas.user import UserCreate, UserBase

router = APIRouter()


@router.post("/users/{page}/{page_size}")
def user_list(
    page: int,
    page_size: int,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    取得使用者列表
    """

    offset = (page - 1) * page_size

    user_list_data = [
        user.to_dict()
        for user in UserModel.get_user_list(
            offset=offset, limit=page_size, db_session=db_session
        )
    ]

    total_rows = db_session.query(UserModel).count()
    return {
        "code": "1",
        "data": {
            "items": user_list_data,
            "rowcount": total_rows,
        },
        "message": "查詢所有用戶成功",
    }


@router.get("/user/{user_id}")
def get_user(
    user_id: str,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    取得使用者資料
    """

    user = UserModel.get_by_user_id(user_id, db_session)

    if not user:
        return {"code": "0", "data": None, "message": "用戶不存在"}

    return {"code": "1", "data": user.to_dict(), "message": "查詢用戶資料成功"}


@router.post("/user")
def create_user(user_data: UserCreate, db_session: Session = Depends(get_db)):
    """
    註冊使用者
    """

    if not user_data.username:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="用戶名稱不得為空")
    if not user_data.email:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="電子郵件不得為空")
    if not user_data.password:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="密碼不得為空")

    email = user_data.email

    user = UserModel.get_by_user_email(email, db_session)

    if user:
        return {
            "code": "0",
            "data": None,
            "message": "用戶已存在",
        }

    user_id = str(uuid.uuid4()).replace("-", "")
    user = UserModel(
        user_id=user_id,
        username=user_data.username,
        age=user_data.age,
        email=user_data.email,
        db_session=db_session,
    )

    password = PasswordModel(
        user_id=user.user_id,
        db_session=db_session,
    )
    password.set_password(user_data.password)

    user.add()
    password.add()

    return {
        "code": "1",
        "data": None,
        "message": "新增用戶成功",
    }


@router.put("/user/{user_id}")
def update_user(
    user_id: str,
    user_data: UserBase,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    更新使用者資料
    """

    if not user_data.user_id:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="用戶編號不得為空")
    if not user_data.username:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="用戶名稱不得為空")
    if not user_data.email:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="電子郵件不得為空")

    existing_user = UserModel.get_by_user_id(user_id, db_session)

    if not existing_user:
        return {
            "code": "0",
            "data": None,
            "message": "用戶不存在",
        }

    existing_user.age = user_data.age
    existing_user.update()

    return {
        "code": "1",
        "data": None,
        "message": "更新用戶成功",
    }


@router.delete("/user/{user_id}")
def delete_user(
    user_id: str,
    current_user=Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    刪除使用者資料
    """

    existing_user = UserModel.get_by_user_id(user_id, db_session)

    if not existing_user:
        return {
            "code": "0",
            "data": None,
            "message": "用戶不存在",
        }

    existing_user.delete()
    return {
        "code": "1",
        "data": None,
        "message": "刪除用戶成功",
    }


@router.post("/faker")
def create_fake_user(db_session: Session = Depends(get_db)):
    """
    註冊大量假的使用者
    """
    fake_user_data = []
    fake_user_password_data = []

    for _ in range(100000):
        user_id = str(uuid.uuid4()).replace("-", "")
        user = UserModel(
            user_id=user_id,
            username="fake_user_" + str(uuid.uuid4()).replace("-", "")[:8],
            age=random.randint(18, 99),
            email=f"fake_email_{uuid.uuid4().hex[:8]}@example.com",
            db_session=db_session,
        )

        password = PasswordModel(
            user_id=user.user_id,
            db_session=db_session,
        )
        password.set_password("fake_password_" + str(uuid.uuid4()).replace("-", "")[:8])

        fake_user_data.append(user)
        fake_user_password_data.append(password)

    db_session.add_all(fake_user_data)
    db_session.add_all(fake_user_password_data)
    db_session.commit()

    return {
        "code": "1",
        "data": None,
        "message": "新增用戶成功",
    }
