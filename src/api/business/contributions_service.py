from typing import List
from fastapi import HTTPException
from datetime import datetime
from io import StringIO
from utilitys.github_helper import GitHubHelper
from utilitys.csv_helper import CsvHelper
from models.contributions import Contribution
from repos.UserDataAccess import UserDataAccess

class ContributionsService:
    def __init__(self):
        """Initialize ContributionsService"""
        self.github_helper = GitHubHelper()
        self.user_repo = UserDataAccess()

    async def export_contributions_csv(self, days: int = 30) -> StringIO:
        """
        Export all active users' GitHub contributions to CSV
        
        Args:
            days: Number of days to look back (default: 30)
            
        Returns:
            StringIO: CSV content as a string buffer
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
            
            # Define headers with desired column order
            headers = {
                'id': 'ID',
                'username': 'Username',
                'contrib_date': 'Date',
                'commit_count': 'Commit Count',
                'pr_review_count': 'PR Review Count',
                'subtotal': 'Total'
            }
            
            # Export to CSV and return stream
            return CsvHelper.export_to_csv(
                data=contributions,
                headers=headers
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export contributions: {str(e)}"
            )