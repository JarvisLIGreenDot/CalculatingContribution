from fastapi import APIRouter

item_router = APIRouter(tags=["items"])

@item_router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "item_name": "Example Item"}