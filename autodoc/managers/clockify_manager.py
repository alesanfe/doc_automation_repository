import difflib
import re
from collections import defaultdict
from datetime import timedelta

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

        detail_report = self._get_detailed_report(selected_ws, members)

        return _append_durations(self._parse_detail_report(detail_report))

    def _get_workspaces(self):
        workspace_service = factories.WorkspaceFactory(api_key=self.token)
        return workspace_service.get_all_workspaces()

    def _filter_workspace(self, workspaces):
        return next(ws for ws in workspaces if self.clockify_ws in ws['name'])

    def _get_workspace_members(self, workspace):
        user_service = factories.UserFactory(api_key=self.token)
        return user_service.get_all_workspace_users(workspace['id'])

    def _get_detailed_report(self, workspace, members):
        time_services = factories.TimeEntryFactory(api_key=self.token)
        return [entry for user in members for entry in time_services.get_all_time_entry_user(workspace['id'], user["id"])]

    def _parse_detail_report(self, time_entries):
        parsed_detail_report = defaultdict(list)
        print(time_entries)
        for entry in time_entries:
            print(entry)
            user_service = factories.UserFactory(api_key=self.token) # TODO: Guardar la información en un diccionario para reducir el número de peticiones.
            user = user_service.get_user(entry['userId'])
            print(user)
            user_name = user['name']
            description = entry['description']
            duration = entry['timeInterval']['duration']
            parsed_detail_report[user_name].append((description, duration))
        return parsed_detail_report





def _append_durations(entries):
    duration_per_description = defaultdict(float)
    print(entries)
    for user, user_entries in entries.items():
        for description, duration in user_entries:
            pattern = r'PT(\d+)H(\d+)M'
            matches = re.match(pattern, duration)
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
            duration = timedelta(hours=hours, minutes=minutes).total_seconds()
            duration_per_description[description] += duration
    return [(description, round(total_duration / 3600, 2)) for description, total_duration in
            duration_per_description.items()]


def _associate_member(member, contributors):
    for contributor in contributors:
        if difflib.SequenceMatcher(None, member['name'], contributor.login).ratio() > 0.5:
            contributor.clockify_id = member['id']


def _associate_members(members, contributors):
    for ws_member in members:
        _associate_member(ws_member, contributors)
