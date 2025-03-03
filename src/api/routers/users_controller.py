from fastapi import APIRouter

user_router = APIRouter(tags=["users"])

@user_router.get("/")
async def read_users():
    return [{"username": "Alice"}, {"username": "Bob"}]