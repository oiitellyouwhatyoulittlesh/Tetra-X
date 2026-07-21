"""
Tetra-X

File:
    json_manager.py

Purpose:
    Handles loading and saving JSON files.

"""

import json
from copy import deepcopy
from pathlib import Path


def load_json(file_path: str, default_data):
    """
    Loads data from a JSON file.

    If the file does not exist, it is created using
    the supplied default data.
    """

    path = Path(file_path)

    if not path.exists():

        path.parent.mkdir(parents=True, exist_ok=True)

        save_json(file_path, default_data)

        return deepcopy(default_data)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path: str, data) -> None:
    """
    Saves data to a JSON file.
    """

    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4
        )
