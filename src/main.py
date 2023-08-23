from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """
        攔截欄位不得為空
        """

        return JSONResponse(
            status_code=exc.status_code,
            content={"code": "0", "data": None, "message": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        攔截欄位缺項 or 錯誤類型
        """

        detail = exc.errors()
        error_messages = [f"{error['loc'][-1]} {error['msg']}" for error in detail]
        error_message = ", ".join(error_messages)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": "0",
                "data": None,
                "detail": exc.errors(),
                "message": error_message,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": "0", "data": None, "message": "內部伺服器錯誤"},
        )

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
