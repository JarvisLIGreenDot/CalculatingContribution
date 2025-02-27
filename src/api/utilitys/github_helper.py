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
    configure_name = "token"

    def __init__(self):
        config_repo = ConfigureDataAccess()
        config = config_repo.get_configuration_by_name(self.configure_name)
        if not config:
            raise ValueError(f"GitHub token not found in configuration with name: {self.configure_name}")
        
        self.github = Github(config.value)

    def get_daily_contributions(self, days: int = 7, users: List[User] = None) -> List[Contribution]:
        """
        Get daily contributions for all users
        Args:
            days: Number of days to look back
            users: List of users to process
        Returns:
            List[Contribution]: Sorted list of daily contributions
        """
        if not users:
            raise ValueError("No users provided to process")
        
        since_date = datetime.now() - timedelta(days=days)
        all_contributions = []
        
        for user_record in users:
            user_contributions = defaultdict(lambda: Contribution(
                username=user_record.account,
                contrib_date=datetime.now().date(),
                commit_count=0,
                pr_review_count=0
            ))
            
            # Search commits directly
            query = f'author:{user_record.account} committer-date:>={since_date.strftime("%Y-%m-%d")}'
            commits = self.github.search_commits(query=query)
            
            for commit in commits:
                date_str = commit.commit.author.date.strftime('%Y-%m-%d')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                user_contributions[date_str].contrib_date = date_obj
                user_contributions[date_str].commit_count += 1

            # Search PR reviews using issues search with type:pr filter
            query = f'type:pr reviewed-by:{user_record.account} updated:>={since_date.strftime("%Y-%m-%d")}'
            pull_requests = self.github.search_issues(query=query)
            
            for pr in pull_requests:
                if hasattr(pr, 'pull_request'):  # Verify it's a PR
                    date_str = pr.updated_at.strftime('%Y-%m-%d')
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    user_contributions[date_str].contrib_date = date_obj
                    user_contributions[date_str].pr_review_count += 1

            # Add non-zero contributions
            daily_contributions = [
                contrib for contrib in user_contributions.values() 
                if contrib.subtotal > 0
            ]
            all_contributions.extend(daily_contributions)
        
        # Sort and add IDs
        sorted_contributions = sorted(
            all_contributions, 
            key=lambda x: (x.contrib_date, x.username),
            reverse=True
        )
        
        for i, contribution in enumerate(sorted_contributions, 1):
            contribution.id = i
        
        return sorted_contributions