from __future__ import annotations

from dataclasses import dataclass
from typing import List

from autodoc.models.Task import Task


@dataclass
class Report:
    user_id: str
    username: str
    tasks: List['Task']
