from fastapi import APIRouter
import socket

router = APIRouter()


@router.get("/")
def hello():
    """
    取得 hostname
    """

    return f"Hello Container World! my hostname is {socket.gethostname()}."
