import difflib
import json
from collections import defaultdict
from typing import List, Tuple

from autodoc import Repository, Report, Contributor
from autodoc.managers.api_manager import APIManager
from clockipy import Clockipy

DEFAULT_URL_OPTIONS = {"front_path": "", "back_path": ""}
REPORT_BASE_URL = "https://reports.api.clockify.me/v1"
DETAILED_FILTER = {"page": 1, "pageSize": 50}
CLOCKIFY_API_REPORTS_BODY = {
    "dateRangeStart": "2023-02-18T00:00:00.000",
    "dateRangeEnd": "2023-03-17T00:00:00.000",
    "detailedFilter": DETAILED_FILTER,
    "exportType": "JSON"
}

class ClockifyManager:
    clockipy: Clockipy
    clockify_url: str
    clockify_ws: str
    repository: Repository
    def get_clockify(self) -> Report:
        workspaces = APIManager.api_call(self.clockipy, self.clockify_url, {}, DEFAULT_URL_OPTIONS)
        selected_ws = ClockifyManager.filter_workspace(workspaces, self.clockify_ws)

        members = ClockifyManager.get_workspace_members(self.clockipy, self.clockify_url, selected_ws)
        ClockifyManager.associate_members(members, self.repository.contributors)

        detail_report = ClockifyManager.get_detailed_report(self.clockipy, self.clockify_url, selected_ws)

        parsed_detail_report = ClockifyManager.parse_detail_report(detail_report['timeentries'])
        parsed_detail_report = ClockifyManager.append_durations(parsed_detail_report)

        return parsed_detail_report

    def filter_workspace(self, workspaces: List):
        return next(ws for ws in workspaces if self.clockify_ws in ws['name'])


    def get_workspace_members(self, selected_ws):
        url_options = DEFAULT_URL_OPTIONS.copy()
        url_options["back_path"] = f"/{selected_ws['id']}/users"
        return APIManager.api_call(self.clockipy, self.clockify_url, {}, url_options)

    def associate_members(self, members, contributors: List[Contributor]) -> None:
        for ws_member in members:
            ClockifyManager.associate_member(ws_member, contributors)


    def associate_member(self, member: json, contributors: List[Contributor]) -> None:
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
        return APIManager.api_call(self.clockipy, self.clockify_url, req_options, url_options)


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