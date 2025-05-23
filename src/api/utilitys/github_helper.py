from datetime import datetime, timedelta
from typing import List, Any
from collections import defaultdict
from github import Github, UnknownObjectException

from models.contribution_detail import ContributionDetail
from repos.ConfigureDataAccess import ConfigureDataAccess
from models.contributions import Contribution
from models.user import User


class GitHubHelper:
    configure_name = "token"

    def __init__(self):
        config_repo = ConfigureDataAccess()
        config = config_repo.get_configuration_by_name(self.configure_name)
        if not config:
            raise ValueError(
                f"GitHub token not found in configuration with name: {self.configure_name}"
            )

        self.github = Github(config.value)

    def get_daily_contributions(
        self, days: int = 7, users: List[User] = None
    ) -> List[Contribution]:
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

        all_contributions = []

        for user_record in users:
            user_contributions = self.get_user_commits_list(days, user_record.account)

            user_pr_contributions = self.get_user_pull_request_list(
                days, user_record.account
            )

            for key, value in user_pr_contributions.items():
                if key in user_contributions:
                    user_contributions[key].pr_review_count += value.pr_review_count
                    user_contributions[key].commit_count += value.commit_count
                else:
                    user_contributions[key] = value

            user_contributions = self.get_user_comtribution_empty_data(
                days, user_record.account, user_contributions
            )

            daily_contributions = list(user_contributions.values())
            all_contributions.extend(daily_contributions)

        # Sort and add IDs - 修改排序逻辑
        sorted_contributions = sorted(
            all_contributions,
            key=lambda x: (
                x.username,
                x.contrib_date,
            ),  # 先按username排序，再按日期排序
            reverse=False,  # 不再反转排序，使得用户名按字母顺序，日期按升序
        )

        for i, contribution in enumerate(sorted_contributions, 1):
            contribution.id = i

        return sorted_contributions

    def get_contribution_details(
        self, days: int = 7, user: User = None
    ) -> List[ContributionDetail]:
        """
        Get detailed contributions for a specific user
        Args:
            days: Number of days to look back
            user: User to process
        Returns:
            List[ContributionDetail]: List of detailed contributions
        """
        if not user:
            raise ValueError("No user provided to process")
        details = []
        commits = self.get_contribution_commits_details(days, user)
        details.append(commits)

        pr_reviews = self.get_contribution_pr_details(days, user)
        details.append(pr_reviews)
        # Sort by date descending
        sorted_details = sorted(
            details, key=lambda x: (x.contrib_date, x.created_date), reverse=True
        )

        # Add sequential IDs
        for i, detail in enumerate(sorted_details, 1):
            detail.id = i

        return sorted_details

    def get_contribution_commits_details(
        self, days: int = 7, user: User = None
    ) -> List[ContributionDetail]:
        since_date = self.get_since_date(days)
        details = []

        # Search commits directly
        query = (
            f"author:{user.account} committer-date:>={since_date.strftime('%Y-%m-%d')}"
        )
        commits = self.github.search_commits(query=query)
        print(f"Found {commits.totalCount} commits for user {user.account}")

        # Process commits
        for commit in commits:
            detail = ContributionDetail(
                username=user.account,
                contrib_date=commit.commit.author.date.date(),
                commit_count=1,
                pr_review_count=0,
                contribution_type="COMMIT",  # 添加此字段
                repo_name=commit.repository.full_name,
                created_date=commit.commit.author.date,
                commit_sha=commit.sha,
                commit_message=commit.commit.message,
                commit_url=commit.html_url,
            )
            details.append(detail)
        return details

    def get_contribution_pr_details(
        self, days: int = 7, user: User = None
    ) -> List[ContributionDetail]:
        since_date = self.get_since_date(days)
        details = []

        # Search PR reviews
        query = f"type:pr reviewed-by:{user.account} updated:>={since_date.strftime('%Y-%m-%d')}"
        pull_requests = self.github.search_issues(query=query)
        print(f"Found {pull_requests.totalCount} PR reviews for user {user.account}")

        # Process PR reviews
        for pr in pull_requests:
            if hasattr(pr, "pull_request"):  # Verify it's a PR
                # 直接使用 issue API 返回的数据，不再获取完整 PR
                detail = ContributionDetail(
                    username=user.account,
                    contrib_date=pr.updated_at.date(),
                    commit_count=0,
                    pr_review_count=1,
                    contribution_type="PR_REVIEW",  # 添加此字段
                    repo_name=pr.repository.full_name,
                    created_date=pr.created_at,
                    pr_number=pr.number,
                    pr_title=pr.title,
                    pr_url=pr.html_url,
                    review_state="APPROVED",  # 简化处理，直接假设为已批准
                )
                details.append(detail)
        return details

    def get_user_commits_list(
        self, days: int = 7, user_account: str = ""
    ) -> defaultdict[Any, Contribution]:
        since_date = self.get_since_date(days)
        try:
            print(f"Check user {user_account} on GitHub")
            self.github.get_user(user_account)
        except UnknownObjectException:
            print(f"User {user_account} not found on GitHub.")

        # 1. 先收集原有贡献数据
        user_contributions = self._init_contribution(user_account)
        query = (
            f"author:{user_account} committer-date:>={since_date.strftime('%Y-%m-%d')}"
        )
        commits = self.github.search_commits(query=query)
        print(f"Found {commits.totalCount} commits for user {user_account}")

        for commit in commits:
            date_str = commit.commit.author.date.strftime("%Y-%m-%d")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            user_contributions[date_str].contrib_date = date_obj
            user_contributions[date_str].commit_count += 1
            user_contributions[date_str].repo_name = commit.repository.full_name

        return user_contributions

    def get_user_pull_request_list(
        self, days: int = 7, user_account: str = ""
    ) -> defaultdict[Any, Contribution]:
        since_date = self.get_since_date(days)
        user_contributions = self._init_contribution(user_account)
        # Search PR reviews using issues search with type:pr filter
        query = f"type:pr reviewed-by:{user_account} updated:>={since_date.strftime('%Y-%m-%d')}"
        pull_requests = self.github.search_issues(query=query)
        print(f"Found {pull_requests.totalCount} PR reviews for user {user_account}")

        for pr in pull_requests:
            if hasattr(pr, "pull_request"):  # Verify it's a PR
                date_str = pr.updated_at.strftime("%Y-%m-%d")
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                user_contributions[date_str].contrib_date = date_obj
                user_contributions[date_str].pr_review_count += 1
                user_contributions[date_str].repo_name = pr.repository.full_name

        return user_contributions

    def _init_contribution(
        self, user_account: str = ""
    ) -> defaultdict[Any, Contribution]:
        user_contributions = defaultdict(
            lambda: Contribution(
                username=user_account,
                contrib_date=datetime.now().date(),
                repo_name="N/A",
                commit_count=0,
                pr_review_count=0,
            )
        )
        return user_contributions

    def get_user_comtribution_empty_data(
        self,
        days: int = 7,
        user_account: str = "",
        user_contributions: defaultdict[Any, Contribution] = None,
    ) -> defaultdict[Any, Contribution]:
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # 计算开始日期：从昨天往前推(days-1)天
        start_date = yesterday - timedelta(days=days-1)
        
        # 初始化从start_date到yesterday的所有日期
        for i in range(days):
            day = start_date + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            if date_str not in user_contributions:
                user_contributions[date_str] = Contribution(
                    username=user_account,
                    contrib_date=day,
                    repo_name="N/A",
                    commit_count=0,
                    pr_review_count=0,
                )
        
        # 移除今天的数据（如果存在）
        today_str = today.strftime("%Y-%m-%d")
        if today_str in user_contributions:
            del user_contributions[today_str]
            
        return user_contributions

    def get_since_date(
            self, days: int = 7
    ) -> datetime:
        since_date = datetime.now() - timedelta(days=days-1)
        return since_date
