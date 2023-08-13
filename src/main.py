from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from src.config import app_config


def create_app(config_name="develop"):
    app = FastAPI()

    class Item(BaseModel):
        name: str
        price: float
        is_offer: Union[bool, None] = None

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.get("/info")
    async def info():
        return {
            "app_name": app_config[config_name].SQLALCHEMY_DATABASE_URI,
        }

    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}

    @app.put("/items/{item_id}")
    def update_item(item_id: int, item: Item):
        return {"item_name": item.name, "item_id": item_id}

    return app


# pip install fastapi
# pip install uvicorn
# pip install 'uvicorn[standard]'
# $env:DATABASE_URL="mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
# uvicorn src.main:create_app --reload
