from typing import List
from fastapi import HTTPException
from repos.RoleDataAccess import RoleDataAccess
from models.role import Role

class RolesService:
    def __init__(self):
        """Initialize RolesService"""
        self.role_repo = RoleDataAccess()

    async def get_all_roles(self) -> List[Role]:
        """
        Get all roles from database
        
        Returns:
            List[Role]: List of all roles
        """
        try:
            roles = self.role_repo.get_roles()
            if not roles:
                raise HTTPException(
                    status_code=404,
                    detail="No roles found"
                )
            return roles
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve roles: {str(e)}"
            )
