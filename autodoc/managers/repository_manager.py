from dataclasses import dataclass
from typing import List

from autodoc import Repository, Commit, Issue, Contributor
from autodoc.managers.api_manager import APIManager

GITHUB_API_HEADERS = {"accept": "application/vnd.github+json"}
DEFAULT_URL_OPTIONS = {"front_path": "", "back_path": ""}

@dataclass
class RepositoryManager:
    octokit: Octokit
    url: str

    def get_repository(self) -> Repository:
        url_options = {"front_path": "/repos", "back_path": ""}
        repository_json = APIManager.api_call(self.octokit, self.url, GITHUB_API_HEADERS, url_options)
        repository = Repository.create(repository_json)

        contributors_url = repository_json['contributors_url']
        repository.contributors = RepositoryManager.get_contributors(self.octokit, contributors_url)

        commits_url = repository_json['commits_url']
        repository.commits = RepositoryManager.get_commits(self.octokit, commits_url)

        issues_url = repository_json['issues_url']
        repository.issues = RepositoryManager.get_issues(self.octokit, issues_url)

        return repository

    def get_contributors(self) -> List[Contributor]:
        contributors_json = APIManager.api_call(self.octokit, self.url, GITHUB_API_HEADERS, DEFAULT_URL_OPTIONS)
        return Contributor.create_contributors(contributors_json)

    def get_commits(self) -> List[Commit]:
        commits_json = APIManager.api_call(self.octokit, self.url, GITHUB_API_HEADERS, DEFAULT_URL_OPTIONS)
        return Commit.create_commits(commits_json)

    def get_issues(self) -> List[Issue]:
        issues_json = APIManager.api_call(self.octokit, self.url, GITHUB_API_HEADERS, DEFAULT_URL_OPTIONS)
        return Issue.create_issues(issues_json)