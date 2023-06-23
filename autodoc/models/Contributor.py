from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Contributor:
    user_id: str
    nickname: str
    url: str
    user_type: str
    site_admin: bool
    contributions: int
    clockify_id: str = ''

    @classmethod
    def create(cls, contributor_json: dict) -> 'Contributor':
        user_id = contributor_json['id']
        nickname = contributor_json['login']
        url = contributor_json['url']
        user_type = contributor_json['type']
        site_admin = contributor_json['site_admin'] == 'true'
        contributions = int(contributor_json['contributions'])
        return cls(user_id, nickname, url, user_type, site_admin, contributions)

    @classmethod
    def create_contributors(cls, contributors_json: list) -> List['Contributor']:
        return [cls.create(c) for c in contributors_json]

    def __str__(self) -> str:
        return self.nickname
