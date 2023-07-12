

from attr import define, field

from autodoc.models import Repository, Commit, Issue, Contributor
from autodoc.managers.api_manager import APIManager
from github import Github, Auth

@define
class RepositoryManager:
    token: str = field()
    url: str
    github: Github = field(init=False)
    repository: Repository = field(init=False)

    @token.validator
    def check_token(self, attribute, value):
        if not value:
            raise ValueError("Token is required")
        if not isinstance(value, str):
            raise ValueError("Token must be a string")
        #if not value.startswith("ghp_"):
        #    raise ValueError("Token must start with ghp_")
        #if len(value) != 40:
        #    raise ValueError("Token must have 40 characters")

    def __attrs_post_init__(self):
        auth = Auth.Token(self.token)
        self.github = Github(auth=auth)

    def get_repository(self) -> Repository:
        return self.github.get_repo(self.url)

