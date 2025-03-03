from typing import List
from fastapi import HTTPException
from datetime import datetime
from io import StringIO
from utilitys.github_helper import GitHubHelper
from utilitys.csv_helper import CsvHelper
from models.contributions import Contribution
from models.contribution_detail import ContributionDetail
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

    async def export_contribution_details_csv(self, days: int = 30, username: str = None) -> StringIO:
        """
        Export detailed GitHub contributions for a specific user to CSV
        
        Args:
            days: Number of days to look back (default: 30)
            username: Username to get details for
            
        Returns:
            StringIO: CSV content as a string buffer
        """
        try:
            if not username:
                raise HTTPException(
                    status_code=400,
                    detail="Username is required"
                )
                
            # Get user from database using account/username
            user = self.user_repo.get_user_by_account(username)
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail=f"User {username} not found"
                )

            # Get contribution details from GitHub
            details = self.github_helper.get_contribution_details(
                days=days,
                user=user
            )
            
            if not details:
                raise HTTPException(
                    status_code=404,
                    detail=f"No contributions found for user {username}"
                )
            
            # Define headers with desired column order
            headers = {
                'id': 'ID',
                'username': 'Username',
                'contrib_date': 'Date',
                'repo_name': 'Repository',
                'created_date': 'Created At',
                'commit_sha': 'Commit SHA',
                'commit_message': 'Commit Message',
                'commit_url': 'Commit URL',
                'pr_number': 'PR Number',
                'pr_title': 'PR Title',
                'pr_url': 'PR URL',
                'review_state': 'Review State'
            }
            
            # Export to CSV and return stream
            return CsvHelper.export_to_csv(
                data=details,
                headers=headers
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export contribution details: {str(e)}"
            )