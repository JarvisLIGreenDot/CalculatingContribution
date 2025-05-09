from fastapi import APIRouter, Depends
from typing import List
from models.teams import Teams
from business.teams_service import TeamsService

teams_router = APIRouter(tags=["teams"])

# 创建TeamsService实例的依赖
def get_teams_service():
    return TeamsService()

@teams_router.get("/", response_model=List[Teams])
async def get_teams(teams_service: TeamsService = Depends(get_teams_service)):
    """
    获取所有团队列表
    """
    return await teams_service.get_all_teams()
