from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return {
        "code": "1",
        "data": None,
        "message": "Hello World",
    }
