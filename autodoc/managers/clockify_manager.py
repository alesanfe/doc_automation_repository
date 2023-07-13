import difflib
from collections import defaultdict

from attr import define, field
from clockify import factories
from github.Repository import Repository





@define
class ClockifyManager:
    token: str = field()
    clockify_ws: str
    repository: Repository

    def get_clockify(self):
        workspaces = self._get_workspaces()
        selected_ws = self._filter_workspace(workspaces)

        members = self._get_workspace_members(selected_ws)
        _associate_members(members, self.repository.get_contributors())

        detail_report = self._get_detailed_report(selected_ws)

        parsed_detail_report = _parse_detail_report(detail_report['timeentries'])
        parsed_detail_report = _append_durations(parsed_detail_report)

        return parsed_detail_report

    def _get_workspaces(self):
        workspace_service = factories.WorkspaceFactory(api_key=self.token)
        return workspace_service.get_workspaces()

    def _filter_workspace(self, workspaces):
        return next(ws for ws in workspaces if self.clockify_ws in ws['name'])

    def _get_workspace_members(self, workspace):
        user_service = factories.UserFactory(api_key=self.token)
        return user_service.get_users(workspace['id'])

    def _get_detailed_report(self, workspace):
        time_services = factories.TimeEntryFactory(api_key=self.token)
        return time_services.get_detailed_report(workspace['id'])


def _parse_detail_report(time_entries):
    parsed_detail_report = defaultdict(list)
    for entry in time_entries:
        user_name = entry['userName']
        description = entry['description']
        duration = entry['timeInterval']['duration']
        parsed_detail_report[user_name].append((description, duration))
    return parsed_detail_report

def _append_durations(entries):
    duration_per_description = defaultdict(float)
    for description, duration in entries:
        duration_per_description[description] += duration
    return [(description, round(total_duration / 3600, 2)) for description, total_duration in duration_per_description.items()]


def _associate_member(member, contributors):
    for contributor in contributors:
        if difflib.SequenceMatcher(None, member['name'], contributor.login).ratio() > 0.5:
            contributor.clockify_id = member['id']


def _associate_members(members, contributors):
    for ws_member in members:
        _associate_member(ws_member, contributors)
