from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import app_config
from src.database import engine, Base
from src.module.resource.hello import router as HelloRouter
from src.module.resource.user import router as UserRouter


def create_app(config_name="develop"):
    """
    啟動 create_app
    """

    Base.metadata.create_all(bind=engine)
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/info")
    async def info():
        """
        測試取得 app_config
        """

        return {
            "app_env": config_name,
            "app_db_name": app_config[config_name].SQLALCHEMY_DATABASE_URL,
        }

    app.include_router(HelloRouter, tags=["Hello"])
    app.include_router(UserRouter, tags=["users"])

    return app


# pip install fastapi
# pip install uvicorn
# pip install 'uvicorn[standard]'
# $env:DATABASE_URL="mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
# uvicorn src.main:create_app --reload
# gunicorn -w 4 --bind=0.0.0.0:8000 -k uvicorn.workers.UvicornWorker src.wsgi:application
# gunicorn -w 4 --bind=0.0.0.0:8000 src.wsgi:application
