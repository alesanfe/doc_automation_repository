from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Issue:
    number: int
    user: str
    title: str
    body: str
    labels: List[str]
    state: str
    assignees: List[str]
    created_at: str
    updated_at: str
    closed_at: str

    @classmethod
    def create(cls, issue_json: dict) -> 'Issue':
        number = issue_json['number']
        user = issue_json['user']['login']
        title = issue_json['title']
        body = issue_json['body']
        labels = [label['name'] for label in issue_json['labels']]
        state = issue_json['state']
        assignees = [assignee['login'] for assignee in issue_json['assignees']]
        created_at = issue_json['created_at']
        updated_at = issue_json['updated_at']
        closed_at = issue_json['closed_at']
        return cls(number, user, title, body, labels, state, assignees, created_at, updated_at, closed_at)

    @classmethod
    def create_issues(cls, issues_json: list) -> List['Issue']:
        return [cls.create(i) for i in issues_json]

    def __str__(self) -> str:
        return f"{self.number}-{self.title}"
