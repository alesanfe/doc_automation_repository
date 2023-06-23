from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class Task:
    user_id: str
    task_id: str
    description: str
    start_date: str
    end_date: str
    duration: str

    @classmethod
    def create(cls, task_json: json) -> 'Task':
        return cls(task_json['userId'], task_json['id'], task_json['description'],
                   task_json['timeInterval']['start'], task_json['timeInterval']['end'],
                   task_json['timeInterval']['duration'])
