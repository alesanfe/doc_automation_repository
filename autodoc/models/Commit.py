from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Commit:
    sha: str
    author: str
    date: str
    message: str

    @classmethod
    def create(cls, commit_json: dict) -> 'Commit':
        sha = commit_json['sha']
        author = commit_json['commit']['author']['name']
        date = commit_json['commit']['author']['date']
        message = commit_json['commit']['message']
        return cls(sha, author, date, message)

    @classmethod
    def create_commits(cls, commits_json: list) -> List['Commit']:
        return [cls.create(c) for c in commits_json]
