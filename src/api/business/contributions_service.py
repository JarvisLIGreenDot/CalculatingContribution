from typing import List
from fastapi import HTTPException
from datetime import datetime
from utilitys.github_helper import GitHubHelper
from utilitys.csv_helper import CsvHelper
from models.contributions import Contribution
from repos.UserDataAccess import UserDataAccess

class ContributionsService:
    def __init__(self):
        """Initialize ContributionsService"""
        self.github_helper = GitHubHelper()
        self.user_repo = UserDataAccess()

    async def export_contributions_csv(self, days: int = 7) -> str:
        """
        Export all active users' GitHub contributions to CSV
        
        Args:
            days: Number of days to look back (default: 30)
            
        Returns:
            str: Path to the generated CSV file
        """
        try:
            # Get active users from database
            users = self.user_repo.get_users()
            if not users:
                raise HTTPException(
                    status_code=404,
                    detail="No active users found"
                )

            # Get contributions from GitHub
            contributions = self.github_helper.get_daily_contributions(
                days=days,
                users=users
            )
            
            if not contributions:
                raise HTTPException(
                    status_code=404,
                    detail="No contributions found"
                )
            
            # Generate filename with date
            filename = f"github_contributions_{datetime.now().strftime('%Y%m%d')}.csv"
            
            # Export to CSV
            filepath = CsvHelper.export_to_csv(contributions, filename)
            
            return filepath
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export contributions: {str(e)}"
            )