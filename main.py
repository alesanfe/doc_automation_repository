import requests

import os


from clockipy.Clockipy import Clockipy
from github import Github, Auth
from autodoc.managers.repository_manager import RepositoryManager
from autodoc.managers.clockify_manager import ClockifyManager


def create_directories() -> str:
    """
    Creates the data directory and its subdirectories if they do not exist.

    Returns:
        The path to the data directory.
    """
    data_path = os.path.join(os.getcwd(), "data")
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    generated_path = os.path.join(data_path, "generated")
    if not os.path.isdir(generated_path):
        os.makedirs(generated_path)
    retrieved_path = os.path.join(data_path, "retrieved")
    if not os.path.isdir(retrieved_path):
        os.makedirs(retrieved_path)
    return data_path


def main():
    owner = input("Enter the owner's name:\n")
    repository = "TODOlist-API2" # input('Enter the repository:\n')
    clockipy_ws = "TODOlist-API2" # input("Enter the clockify's workspace name:\n")
    full_name = owner + "/" + repository
    data_path = create_directories()
    # Api-Key Configuration
    with open(r".\autodoc\token.txt", "r") as token_file:
        line = token_file.readline()
        github_key, clokify_key = line.split(";")
    try:
        repository = RepositoryManager(github_key, full_name).get_repository()
        print(repository)
        clockify_report = ClockifyManager(clokify_key, clockipy_ws, repository).get_clockify()

        # templates_path = os.getcwd() + '/templates/'
        # template_name = 'repository_test_template.txt'
        # to_markdown(repository, templates_path, template_name)

    except (ValueError, ConnectionError) as error:
        print(error)
    input('Press Enter to exit...')


if __name__ == '__main__':
    main()
