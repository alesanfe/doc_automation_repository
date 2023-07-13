import os
from dataclasses import dataclass
from typing import List

from github.Repository import Repository


@dataclass
class MarkdownConverter:
    repository: Repository
    workspace: dict
    templates_path: str
    out_path: str

    def to_markdown(self) -> None:
        if not os.path.exists(self.templates_path) or not os.path.isdir(self.templates_path):
            raise ValueError("Could not find templates directory!")

        # file_path = template_name.replace('.txt', '.md')
        # self.save_file(self.templates_path + file_path, filled_template)
        file_handler = FileHandler(self.templates_path + "task_template.txt", self.out_path + "task.md")

        task_template = file_handler.read_file()
        tasks = [self.fill_task(issue, task_template) for issue in self.repository.issues]
        print(tasks)

        file_handler.save_file(tasks)

    def replace_template_variables(self, line):
        start_index = line.rfind("{") + 1
        end_index = line.rfind("}")
        pointer = line[start_index:end_index]
        value = str(getattr(self.repository, pointer))
        return line.replace("{" + pointer + "}", value)

    def fill_task(self, issue: "Issue", task_template: str) -> str:
        # TODO
        print(issue.user)
        print(self.workspace.get(issue.user))
        return ""


    def fill_base(self, empty_template: List[str]) -> List[str]:
        filled_template = [self.replace_template_variables(line)
                           if "{" in line and "}" in line else line for line in empty_template]
        return filled_template

@dataclass
class FileHandler:
    in_path: str
    out_path: str

    def read_file(self) -> List[str]:
        with open(self.in_path, "r") as file:
            empty_template = file.readlines()
        return empty_template

    def save_file(self, data: List[str]) -> None:
        with open(self.out_path, "w") as file:
            file.writelines(data)

