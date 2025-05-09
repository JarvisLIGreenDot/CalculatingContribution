from typing import List
from fastapi import HTTPException
from repos.UserDataAccess import UserDataAccess
from models.user import User

class UsersService:
    def __init__(self):
        """Initialize UsersService"""
        self.user_repo = UserDataAccess()

    async def get_all_users(self) -> List[User]:
        """
        Get all active users from database
        
        Returns:
            List[User]: List of all active users
        """
        try:
            users = self.user_repo.get_users()
            if not users:
                raise HTTPException(
                    status_code=404,
                    detail="No active users found"
                )
            return users
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve users: {str(e)}"
            )
