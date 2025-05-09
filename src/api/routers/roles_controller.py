from fastapi import APIRouter, Depends
from typing import List
from models.role import Role
from business.roles_service import RolesService

roles_router = APIRouter(prefix="/api/roles", tags=["roles"])

# 创建RolesService实例的依赖
def get_roles_service():
    return RolesService()

@roles_router.get("/list")
async def get_roles(roles_service: RolesService = Depends(get_roles_service)):
    """
    获取所有角色列表
    """
    return await roles_service.get_all_roles()
