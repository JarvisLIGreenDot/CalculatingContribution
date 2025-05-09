from fastapi import APIRouter, Depends
from typing import List
from models.user import User
from business.users_service import UsersService

user_router = APIRouter(prefix="/api/users", tags=["users"])

# 创建UsersService实例的依赖
def get_users_service():
    return UsersService()

@user_router.get("/list")
async def get_users(users_service: UsersService = Depends(get_users_service)):
    """
    获取所有活跃用户列表
    """
    return await users_service.get_all_users()