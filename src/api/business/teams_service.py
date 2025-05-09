from typing import List
from fastapi import HTTPException
from repos.TeamsDataAccess import TeamsDataAccess
from models.teams import Teams

class TeamsService:
    def __init__(self):
        """Initialize TeamsService"""
        self.teams_repo = TeamsDataAccess()

    async def get_all_teams(self) -> List[Teams]:
        """
        Get all teams from database
        
        Returns:
            List[Teams]: List of all teams
        """
        try:
            teams = self.teams_repo.get_teams()
            if not teams:
                raise HTTPException(
                    status_code=404,
                    detail="No teams found"
                )
            return teams
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve teams: {str(e)}"
            )
