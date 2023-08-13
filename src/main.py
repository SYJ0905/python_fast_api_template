# from typing import Union
from fastapi import FastAPI

# from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.config import app_config

from src.module.resource.hello import router


def create_app(config_name="develop"):
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(CORSMiddleware, allow_origins=origins)

    # class Item(BaseModel):
    #     name: str
    #     price: float
    #     is_offer: Union[bool, None] = None

    @app.get("/info")
    async def info():
        return {
            "app_env": config_name,
            "app_db_name": app_config[config_name].SQLALCHEMY_DATABASE_URI,
        }

    # @app.get("/items/{item_id}")
    # def read_item(item_id: int, q: Union[str, None] = None):
    #     return {"item_id": item_id, "q": q}

    # @app.put("/items/{item_id}")
    # def update_item(item_id: int, item: Item):
    #     return {"item_name": item.name, "item_id": item_id}

    app.include_router(router)

    return app


# pip install fastapi
# pip install uvicorn
# pip install 'uvicorn[standard]'
# $env:DATABASE_URL="mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
# uvicorn src.main:create_app --reload


# gunicorn -w 4 --bind=0.0.0.0:8000 -k uvicorn.workers.UvicornWorker src.wsgi:application
# gunicorn -w 4 --bind=0.0.0.0:8000 src.wsgi:application
