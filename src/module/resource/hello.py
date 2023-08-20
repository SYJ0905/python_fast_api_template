from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()


@router.get("/")
def read_root():
    return {
        "code": "1",
        "data": None,
        "message": "Hello World",
    }


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@router.post(
    "/test/{item_id}",
    tags=["test"],
    summary="摘要",
    # description="描述",
)
async def create_item(
    item_id: int,
    item: Item,
    needy: str,
    limit: int | None = 10,
    query: str
    | None = Query(
        default=None,
        title="Query title",
        description="Query description",
        deprecated=False,
    ),
    # q: str | None = Query(min_length=3, max_length=10),
    # q: str | None = Query(default=None, min_length=3, max_length=10),
):
    """
    Create an item with all the information:

    - **測試**: 敘述
    """
    return {
        "item_id": item_id,
        "item": item.model_dump(),
        "limit": limit,
        "needy": needy,
        "query": query,
        **item.model_dump(),
    }
