from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from github import Github
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser
from repos.ConfigureDataAccess import ConfigureDataAccess
from models.contributions import Contribution
from repos.UserDataAccess import UserDataAccess
from models.user import User

class GitHubHelper:
    def __init__(self):
        """Initialize GitHub helper using token from configuration"""
        config_repo = ConfigureDataAccess()
        config = config_repo.get_configuration_by_key("github.token")
        if not config:
            raise ValueError("GitHub token not found in configuration")
        
        self.github = Github(config.value)
        
    def get_daily_contributions(self, days: int = 7) -> List[Contribution]:
        """
        Get daily contributions for all active users, grouped by user and date
        Args:
            days: Number of days to look back (default: 7)
        Returns:
            List[Contribution]: List of daily contributions grouped by user and date
        """
        user_repo = UserDataAccess()
        users = user_repo.get_users()
        
        if not users:
            raise ValueError("No users found to process")
        
        since_date = datetime.now() - timedelta(days=days)
        all_contributions = []
        
        # Process each user
        for user_record in users:
            github_user = self.github.get_user(user_record.account)
            user_contributions = defaultdict(lambda: Contribution(
                username=user_record.account,
                contrib_date=datetime.now().date(),
                commit_count=0,
                pr_review_count=0
            ))
            
            # Get user's repositories
            for repo in github_user.get_repos():
                self._collect_daily_repo_contributions(
                    repo, github_user, since_date, user_contributions
                )
            
            # Add non-zero contributions to result
            daily_contributions = [
                contrib for contrib in user_contributions.values() 
                if contrib.subtotal > 0
            ]
            all_contributions.extend(daily_contributions)
        
        # Sort by username first, then by date
        return sorted(
            all_contributions, 
            key=lambda x: (x.username, x.contrib_date)
        )
    
    def _collect_daily_repo_contributions(
        self, 
        repo: Repository, 
        user: AuthenticatedUser, 
        since_date: datetime,
        contributions_dict: defaultdict
    ) -> None:
        """Collect daily contributions for a specific repository"""
        
        # Count commits
        try:
            commits = repo.get_commits(author=user, since=since_date)
            for commit in commits:
                date_str = commit.commit.author.date.strftime('%Y-%m-%d')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                contributions_dict[date_str].contrib_date = date_obj
                contributions_dict[date_str].commit_count += 1
        except Exception:
            pass
            
        # Count pull requests
        try:
            pulls = repo.get_pulls(state='all', creator=user)
            for pr in pulls:
                if pr.created_at >= since_date:
                    date_str = pr.created_at.strftime('%Y-%m-%d')
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    contributions_dict[date_str].contrib_date = date_obj
                    contributions_dict[date_str].pr_review_count += 1
        except Exception:
            pass