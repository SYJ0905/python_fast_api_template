from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.module.resource.main import router as mainRouter
from src.module.resource.auth import router as AuthRouter
from src.module.resource.user import router as UserRouter
from src.module.resource.message import router as MessageRouter

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
async def validation_exception_handler(request: Request, exc: RequestValidationError):
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
        content={
            "code": "0",
            "data": None,
            " message": "內部伺服器錯誤",
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mainRouter, tags=["hello"])
app.include_router(AuthRouter, tags=["auth"])
app.include_router(UserRouter, tags=["users"])
app.include_router(MessageRouter, tags=["message"])

# 預設本地 MySQL
# $env:DATABASE_URL="mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
# uvicorn src.main:app --reload --port 8000

# 指定 Docker MySQL
# uvicorn src.main:app --reload --port 8001

# 雲端部署
# gunicorn -w 4 --bind=0.0.0.0:8000 -k uvicorn.workers.UvicornWorker src.main:app
# gunicorn -w 4 --bind=0.0.0.0:8000 src.main:app
