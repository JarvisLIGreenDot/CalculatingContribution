from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from github import Github
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser

class GitHubHelper:
    def __init__(self, access_token: str):
        """Initialize GitHub helper with access token"""
        self.github = Github(access_token)
        
    def get_daily_contributions(self, username: str, days: int = 365) -> Dict:
        """
        Get user's daily contributions for the specified period
        Args:
            username: GitHub username
            days: Number of days to look back (default: 365)
        Returns:
            Dict containing daily contribution statistics
        """
        user = self.github.get_user(username)
        since_date = datetime.now() - timedelta(days=days)
        
        # Initialize daily contributions structure
        daily_contributions = defaultdict(lambda: {
            "date": "",
            "commits": 0,
            "pull_requests": 0,
            "issues": 0,
            "total": 0
        })
        
        # Get user's repositories
        for repo in user.get_repos():
            self._collect_daily_repo_contributions(
                repo, user, since_date, daily_contributions
            )
        
        # Convert defaultdict to regular dict and sort by date
        result = {
            "daily_data": sorted(
                daily_contributions.values(), 
                key=lambda x: x["date"]
            ),
            "summary": {
                "total_commits": sum(day["commits"] for day in daily_contributions.values()),
                "total_prs": sum(day["pull_requests"] for day in daily_contributions.values()),
                "total_issues": sum(day["issues"] for day in daily_contributions.values())
            }
        }
        
        return result
    
    def _collect_daily_repo_contributions(
        self, 
        repo: Repository, 
        user: AuthenticatedUser, 
        since_date: datetime,
        daily_contributions: defaultdict
    ) -> None:
        """Collect daily contributions for a specific repository"""
        
        # Count commits
        try:
            commits = repo.get_commits(author=user, since=since_date)
            for commit in commits:
                date_str = commit.commit.author.date.strftime('%Y-%m-%d')
                daily_contributions[date_str]["date"] = date_str
                daily_contributions[date_str]["commits"] += 1
                daily_contributions[date_str]["total"] += 1
        except Exception:
            pass
            
        # Count pull requests
        try:
            pulls = repo.get_pulls(state='all', creator=user)
            for pr in pulls:
                if pr.created_at >= since_date:
                    date_str = pr.created_at.strftime('%Y-%m-%d')
                    daily_contributions[date_str]["date"] = date_str
                    daily_contributions[date_str]["pull_requests"] += 1
                    daily_contributions[date_str]["total"] += 1
        except Exception:
            pass
            
        # Count issues
        try:
            issues = repo.get_issues(creator=user)
            for issue in issues:
                if issue.created_at >= since_date:
                    date_str = issue.created_at.strftime('%Y-%m-%d')
                    daily_contributions[date_str]["date"] = date_str
                    daily_contributions[date_str]["issues"] += 1
                    daily_contributions[date_str]["total"] += 1
        except Exception:
            pass