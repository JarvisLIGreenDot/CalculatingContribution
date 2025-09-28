from datetime import datetime, timedelta
from typing import List, Any, Tuple
from collections import defaultdict
from github import Github, UnknownObjectException

from models.contribution_detail import ContributionDetail
from repos.ConfigureDataAccess import ConfigureDataAccess
from models.contributions import Contribution
from models.user import User


class GitHubDateRangeHelper:
    configure_name = "token"

    def __init__(self):
        config_repo = ConfigureDataAccess()
        config = config_repo.get_configuration_by_name(self.configure_name)
        if not config:
            raise ValueError(
                f"GitHub token not found in configuration with name: {self.configure_name}"
            )

        self.github = Github(config.value)

    def _parse_and_prepare_dates(
            self, start_date_str: str, end_date_str: str
    ) -> Tuple[datetime.date, datetime.date]:
        """Parses date strings and sets defaults if they are not provided."""
        date_format = "%Y-%m-%d"

        if end_date_str:
            end_date = datetime.strptime(end_date_str, date_format).date()
        else:
            end_date = datetime.now().date()

        if start_date_str:
            start_date = datetime.strptime(start_date_str, date_format).date()
        else:
            # Default to a 7-day period ending on the end_date
            start_date = end_date - timedelta(days=6)

        return start_date, end_date

    def get_daily_contributions(
            self, start_date: str = "", end_date: str = "", users: List[User] = None
    ) -> List[Contribution]:
        """
        Get daily contributions for all users within a date range.
        Args:
            start_date: The start date in 'YYYY-MM-DD' format. Defaults to 7 days before end_date.
            end_date: The end date in 'YYYY-MM-DD' format. Defaults to today.
            users: List of users to process.
        Returns:
            List[Contribution]: Sorted list of daily contributions.
        """
        if not users:
            raise ValueError("No users provided to process")

        start_date_obj, end_date_obj = self._parse_and_prepare_dates(start_date, end_date)
        all_contributions = []

        for user_record in users:
            user_contributions = self.get_user_commits_list(
                start_date_obj, end_date_obj, user_record.account
            )
            user_pr_contributions = self.get_user_pull_request_list(
                start_date_obj, end_date_obj, user_record.account
            )

            for key, value in user_pr_contributions.items():
                if key in user_contributions:
                    user_contributions[key].pr_review_count += value.pr_review_count
                else:
                    user_contributions[key] = value

            user_contributions = self.get_user_contribution_empty_data(
                start_date_obj, end_date_obj, user_record.account, user_contributions
            )

            all_contributions.extend(list(user_contributions.values()))

        sorted_contributions = sorted(
            all_contributions, key=lambda x: (x.username, x.contrib_date)
        )

        for i, contribution in enumerate(sorted_contributions, 1):
            contribution.id = i

        return sorted_contributions

    def get_contribution_details(
            self, start_date: str = "", end_date: str = "", user: User = None
    ) -> List[ContributionDetail]:
        """
        Get detailed contributions for a specific user within a date range.
        Args:
            start_date: The start date in 'YYYY-MM-DD' format.
            end_date: The end date in 'YYYY-MM-DD' format.
            user: User to process.
        Returns:
            List[ContributionDetail]: List of detailed contributions.
        """
        if not user:
            raise ValueError("No user provided to process")

        start_date_obj, end_date_obj = self._parse_and_prepare_dates(start_date, end_date)
        details = []

        commits = self.get_contribution_commits_details(start_date_obj, end_date_obj, user)
        details.extend(commits)

        pr_reviews = self.get_contribution_pr_details(start_date_obj, end_date_obj, user)
        details.extend(pr_reviews)

        sorted_details = sorted(
            details, key=lambda x: (x.contrib_date, x.created_date), reverse=True
        )

        for i, detail in enumerate(sorted_details, 1):
            detail.id = i

        return sorted_details

    def get_contribution_commits_details(
            self, start_date: datetime.date, end_date: datetime.date, user: User = None
    ) -> List[ContributionDetail]:
        details = []
        date_format = "%Y-%m-%d"
        query = (
            f"author:{user.account} "
            f"committer-date:{start_date.strftime(date_format)}..{end_date.strftime(date_format)}"
        )
        commits = self.github.search_commits(query=query)
        print(f"Found {commits.totalCount} commits for user {user.account}")

        for commit in commits:
            details.append(ContributionDetail(
                username=user.account,
                contrib_date=commit.commit.author.date.date(),
                commit_count=1,
                pr_review_count=0,
                contribution_type="COMMIT",
                repo_name=commit.repository.full_name,
                created_date=commit.commit.author.date,
                commit_sha=commit.sha,
                commit_message=commit.commit.message,
                commit_url=commit.html_url,
            ))
        return details

    def get_contribution_pr_details(
            self, start_date: datetime.date, end_date: datetime.date, user: User = None
    ) -> List[ContributionDetail]:
        details = []
        date_format = "%Y-%m-%d"
        query = (
            f"type:pr reviewed-by:{user.account} "
            f"updated:{start_date.strftime(date_format)}..{end_date.strftime(date_format)}"
        )
        pull_requests = self.github.search_issues(query=query)
        print(f"Found {pull_requests.totalCount} PR reviews for user {user.account}")

        for pr in pull_requests:
            if hasattr(pr, "pull_request"):
                details.append(ContributionDetail(
                    username=user.account,
                    contrib_date=pr.updated_at.date(),
                    commit_count=0,
                    pr_review_count=1,
                    contribution_type="PR_REVIEW",
                    repo_name=pr.repository.full_name,
                    created_date=pr.created_at,
                    pr_number=pr.number,
                    pr_title=pr.title,
                    pr_url=pr.html_url,
                    review_state="APPROVED",
                ))
        return details

    def get_user_commits_list(
            self, start_date: datetime.date, end_date: datetime.date, user_account: str = ""
    ) -> defaultdict[Any, Contribution]:
        user_contributions = self._init_contribution(user_account)
        date_format = "%Y-%m-%d"
        query = (
            f"author:{user_account} "
            f"committer-date:{start_date.strftime(date_format)}..{end_date.strftime(date_format)}"
        )
        commits = self.github.search_commits(query=query)
        print(f"Found {commits.totalCount} commits for user {user_account}")

        for commit in commits:
            date_str = commit.commit.author.date.strftime(date_format)
            user_contributions[date_str].contrib_date = commit.commit.author.date.date()
            user_contributions[date_str].commit_count += 1
            user_contributions[date_str].repo_name = commit.repository.full_name

        return user_contributions

    def get_user_pull_request_list(
            self, start_date: datetime.date, end_date: datetime.date, user_account: str = ""
    ) -> defaultdict[Any, Contribution]:
        user_contributions = self._init_contribution(user_account)
        date_format = "%Y-%m-%d"
        query = (
            f"type:pr reviewed-by:{user_account} "
            f"updated:{start_date.strftime(date_format)}..{end_date.strftime(date_format)}"
        )
        pull_requests = self.github.search_issues(query=query)
        print(f"Found {pull_requests.totalCount} PR reviews for user {user_account}")

        for pr in pull_requests:
            if hasattr(pr, "pull_request"):
                date_str = pr.updated_at.strftime(date_format)
                user_contributions[date_str].contrib_date = pr.updated_at.date()
                user_contributions[date_str].pr_review_count += 1
                user_contributions[date_str].repo_name = pr.repository.full_name

        return user_contributions

    def _init_contribution(
            self, user_account: str = ""
    ) -> defaultdict[Any, Contribution]:
        return defaultdict(
            lambda: Contribution(
                username=user_account,
                contrib_date=datetime.now().date(),
                repo_name="N/A",
                commit_count=0,
                pr_review_count=0,
            )
        )

    def get_user_contribution_empty_data(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            user_account: str = "",
            user_contributions: defaultdict[Any, Contribution] = None,
    ) -> defaultdict[Any, Contribution]:

        delta = end_date - start_date
        for i in range(delta.days + 1):
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
        return user_contributions