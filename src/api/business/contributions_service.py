from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from utilitys.github_helper import GitHubHelper
from utilitys.csv_helper import CsvHelper
from models.contributions import Contribution

class ContributionsService:
    def __init__(self, session: Session):
        self.session = session
        self.github_helper = GitHubHelper(session)

    async def export_contributions_csv(self, username: str, days: int = 365) -> str:
        """
        Export user's GitHub contributions to CSV
        
        Args:
            username: GitHub username
            days: Number of days to look back (default: 365)
            
        Returns:
            str: Path to the generated CSV file
        """
        try:
            # Get contributions data from GitHub
            contributions = self.github_helper.get_daily_contributions(username, days)
            
            if not contributions:
                raise HTTPException(
                    status_code=404,
                    detail=f"No contributions found for user {username}"
                )
            
            # Generate filename with username and date
            filename = f"github_contributions_{username}_{datetime.now().strftime('%Y%m%d')}.csv"
            
            # Export to CSV
            filepath = CsvHelper.export_to_csv(contributions, filename)
            
            return filepath
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export contributions: {str(e)}"
            )