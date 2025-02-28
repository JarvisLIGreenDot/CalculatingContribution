from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Contribution:
    username: str
    contrib_date: date
    commit_count: int = 0
    pr_review_count: int = 0
    id: Optional[int] = None

    @property
    def subtotal(self) -> int:
        return self.commit_count + self.pr_review_count