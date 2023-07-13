import requests

import os

import tkinter as tk
from tkinter import messagebox

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
    owner = owner_entry.get()
    repository = repository_entry.get()
    clockipy_ws = clockify_ws_entry.get()
    github_key = github_key_entry.get()
    clokify_key = clokify_key_entry.get()
    owner = "alesanfe"
    repository = "TODOlist-API2"
    clockipy_ws = "TODOlist-API2"
    github_key = "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"
    clokify_key = "OGViNzFhMjMtOWVkZS00NWU2LWE2ZjUtYmU4ZmM1MThkYzUy"
    full_name = owner + "/" + repository
    data_path = create_directories()

    repository = RepositoryManager(github_key, full_name).get_repository()
    print(repository)
    clockify_report = ClockifyManager(clokify_key, clockipy_ws, repository).get_clockify()

    # templates_path = os.getcwd() + '/templates/'
    # template_name = 'repository_test_template.txt'
    # to_markdown(repository, templates_path, template_name)


def submit():
    try:
        main()
        messagebox.showinfo("Success", "Proceso completado exitosamente")
    except Exception as e:
        raise e
        messagebox.showerror("Error", str(e))



if __name__ == '__main__':
    # Crear la ventana principal
    window = tk.Tk()
    window.title("Interfaz para doc automatation")
    window.geometry("200x250")

    # Crear los elementos de la interfaz
    owner_label = tk.Label(window, text="Owner's name:")
    owner_label.pack()
    owner_entry = tk.Entry(window)
    owner_entry.pack()

    repository_label = tk.Label(window, text="Repository's name:")
    repository_label.pack()
    repository_entry = tk.Entry(window)
    repository_entry.pack()

    clockify_ws_label = tk.Label(window, text="Clockify's workspace:")
    clockify_ws_label.pack()
    clockify_ws_entry = tk.Entry(window)
    clockify_ws_entry.pack()

    github_key_label = tk.Label(window, text="Github's key:")
    github_key_label.pack()
    github_key_entry = tk.Entry(window)
    github_key_entry.pack()

    clokify_key_label = tk.Label(window, text="Clockify's key:")
    clokify_key_label.pack()
    clokify_key_entry = tk.Entry(window)
    clokify_key_entry.pack()

    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.pack()

    # Iniciar el bucle de eventos
    window.mainloop()
