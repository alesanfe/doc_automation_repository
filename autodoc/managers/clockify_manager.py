from dataclasses import dataclass
from typing import List, Tuple
from collections import defaultdict
import difflib

from attr import define, field

from autodoc.managers.api_manager import APIManager
from autodoc.models import Repository, Contributor
from autodoc.models.Report import Report
from clockipy.Clockipy import Clockipy

DEFAULT_URL_OPTIONS = {"front_path": "", "back_path": ""}
REPORT_BASE_URL = "https://reports.api.clockify.me/v1"
DETAILED_FILTER = {"page": 1, "pageSize": 50}
CLOCKIFY_API_REPORTS_BODY = {
    "dateRangeStart": "2023-02-18T00:00:00.000",
    "dateRangeEnd": "2023-03-17T00:00:00.000",
    "detailedFilter": DETAILED_FILTER,
    "exportType": "JSON"
}

@define
class ClockifyManager:
    token: str = field()
    clockify_ws: str
    repository: Repository
    clockify_url: str = field(default="https://api.clockify.me/api/v1/workspaces")

    @token.validator
    def check_token(self, attribute, value):
        if not value:
            raise ValueError("Token is required")
        if not isinstance(value, str):
            raise ValueError("Token must be a string")
        if len(value) != 48:
            raise ValueError("Token must have 48 characters")

    @clockify_url.validator
    def check_clockify_url(self, attribute, value):
        if not value:
            raise ValueError("Clockify url is required")
        if not isinstance(value, str):
            raise ValueError("Clockify url must be a string")


    def __post_init__(self):
        self.clockipy = Clockipy(self.token)

    def get_clockify(self) -> Report:
        workspaces = APIManager.api_call(self.clockify_url)
        selected_ws = self.filter_workspace(workspaces)

        members = self.get_workspace_members(selected_ws)
        self.associate_members(members, self.repository.contributors)

        detail_report = self.get_detailed_report(selected_ws)

        parsed_detail_report = self.parse_detail_report(detail_report['timeentries'])
        parsed_detail_report = self.append_durations(parsed_detail_report)

        return parsed_detail_report

    def filter_workspace(self, workspaces: List):
        return next(ws for ws in workspaces if self.clockify_ws in ws['name'])

    def get_workspace_members(self, selected_ws):
        url_options = DEFAULT_URL_OPTIONS.copy()
        url_options["back_path"] = f"/{selected_ws['id']}/users"
        return APIManager.api_call(self.clockipy, self.clockify_url, url_options)

    def associate_members(self, members, contributors: List[Contributor]) -> None:
        for ws_member in members:
            self.associate_member(ws_member, contributors)

    def associate_member(self, member, contributors: List[Contributor]) -> None:
        for contributor in contributors:
            if difflib.SequenceMatcher(None, member['name'], contributor.nickname).ratio() > 0.5:
                contributor.clockify_id = member['id']

    def get_detailed_report(self, selected_ws):
        url_options = DEFAULT_URL_OPTIONS.copy()
        url_options["back_path"] = f"/{selected_ws['id']}/reports/detailed"
        url_options["report"] = True
        req_options = {
            "base_url": REPORT_BASE_URL,
            "body": CLOCKIFY_API_REPORTS_BODY
        }
        return APIManager.api_call(self.clockipy, self.clockify_url, url_options)

    def parse_detail_report(self, time_entries):
        parsed_detail_report = defaultdict(list)
        for entry in time_entries:
            user_name = entry['userName']
            description = entry['description']
            duration = entry['timeInterval']['duration']
            parsed_detail_report[user_name].append((description, duration))
        return parsed_detail_report

    def append_durations(self, entries: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        duration_per_description = defaultdict(float)
        for description, duration in entries:
            duration_per_description[description] += duration
        return [(description, round(total_duration / 3600, 2)) for description, total_duration in duration_per_description.items()]