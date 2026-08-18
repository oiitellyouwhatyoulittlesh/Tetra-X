"""
Tetra-X

File:
    records.py

Purpose:
    Handles persistent personal records.
"""

import json
from copy import deepcopy
from pathlib import Path

from constants import DEFAULT_RECORDS

# ====================
# File Path Definitions
# ====================

RECORDS_FILE = Path(__file__).resolve().parents[2] / "records.json"


# ====================
# Loading Operations
# ====================

def load_records() -> dict:
    """
    Loads records from the external JSON file.

    If the file does not exist or is invalid, default records are returned.
    """
    if not RECORDS_FILE.exists():
        save_records(DEFAULT_RECORDS)
        return deepcopy(DEFAULT_RECORDS)

    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)
    except (OSError, json.JSONDecodeError):
        save_records(DEFAULT_RECORDS)
        return deepcopy(DEFAULT_RECORDS)

    # Missing Data Safety Fallbacks
    if "blitz" not in records:
        records["blitz"] = DEFAULT_RECORDS["blitz"].copy()

    if "forty_lines" not in records:
        records["forty_lines"] = DEFAULT_RECORDS["forty_lines"].copy()

    return records


# ====================
# Saving Operations
# ====================

def save_records(records: dict) -> None:
    """
    Saves records to the external JSON file.
    """
    try:
        with open(RECORDS_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
    except OSError:
        pass


# ====================
# Blitz Mode Records
# ====================

def get_blitz_record() -> dict:
    """
    Returns the current Blitz personal best dictionary.
    """
    records = load_records()
    return records["blitz"]


def update_blitz_record(run: dict) -> bool:
    """
    Updates the Blitz record if the run has a higher score.

    Returns True if a new record was set.
    """
    records = load_records()
    current_record = records["blitz"]

    if run["score"] <= current_record["score"]:
        return False

    records["blitz"] = run
    save_records(records)

    return True


# ====================
# 40 Lines Mode Records
# ====================

def get_forty_lines_record() -> dict:
    """
    Returns the current 40 Lines personal best dictionary.
    """
    records = load_records()
    return records["forty_lines"]


def update_forty_lines_record(run: dict) -> bool:
    """
    Updates the 40 Lines record if the run has a faster completion time.

    Returns True if a new record was set.
    """
    records = load_records()
    current_record = records["forty_lines"]
    current_time = current_record["time"]

    # First Completed Run Handling
    if current_time is None:
        records["forty_lines"] = run
        save_records(records)
        return True

    # Check Faster Completion Time
    if run["time"] >= current_time:
        return False

    records["forty_lines"] = run
    save_records(records)

    return True
