from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from models.contributions import Contribution

@dataclass
class ContributionDetail(Contribution):
    repo_name: str = ''  # 仓库名称
    created_date: datetime = None  # 创建时间
    contribution_type: str = ''  # 贡献类型（COMMIT/PR_REVIEW）
    pr_number: Optional[int] = None  # PR编号
    pr_title: str = ''  # PR标题
    pr_url: str = ''  # PR链接
    review_state: str = ''  # Review状态 (APPROVED/CHANGES_REQUESTED/COMMENTED)
    commit_sha: str = ''  # Commit SHA
    commit_message: str = ''  # Commit信息
    commit_url: str = ''  # Commit链接

    def __post_init__(self):
        # 确保父类的字段被正确初始化
        if not hasattr(self, 'username'):
            self.username = ''
        if not hasattr(self, 'contrib_date'):
            self.contrib_date = date.today()
        if not hasattr(self, 'commit_count'):
            self.commit_count = 0
        if not hasattr(self, 'pr_review_count'):
            self.pr_review_count = 0
        if not hasattr(self, 'id'):
            self.id = None
        
        # 自动推断贡献类型（如果未提供）
        if not self.contribution_type:
            if self.commit_sha:
                self.contribution_type = "COMMIT"
            elif self.pr_number:
                self.contribution_type = "PR_REVIEW"