import schedule
import time
from datetime import datetime
from typing import List

from utilitys.github_helper import GitHubHelper
from config.load_config import app_settings

class ContributionTask:
    def __init__(self, github_token: str, usernames: List[str]):
        """
        Initialize contribution task
        Args:
            github_token: GitHub personal access token
            usernames: List of GitHub usernames to track
        """
        self.github_helper = GitHubHelper(github_token)
        self.usernames = usernames
        
    def fetch_contributions(self):
        """Fetch contributions for all tracked users"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Starting contribution fetch...")
        
        for username in self.usernames:
            try:
                contributions = self.github_helper.get_daily_contributions(username)
                # TODO: Save contributions to database
                print(f"Fetched contributions for {username}")
                print(f"Total commits: {contributions['summary']['total_commits']}")
                print(f"Total PRs: {contributions['summary']['total_prs']}")
                print(f"Total issues: {contributions['summary']['total_issues']}")
            except Exception as e:
                print(f"Error fetching contributions for {username}: {str(e)}")
                
        print(f"[{timestamp}] Contribution fetch completed")

def start_contribution_task():
    """Initialize and start the contribution tracking task"""
    # TODO: Load these from configuration
    github_token = "your_github_token"
    usernames = ["username1", "username2"]
    
    # Create task instance
    task = ContributionTask(github_token, usernames)
    
    # Schedule daily runs at specific time (e.g., 1:00 AM)
    schedule.every().day.at("01:00").do(task.fetch_contributions)
    
    # Run immediately on start
    task.fetch_contributions()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_contribution_task()