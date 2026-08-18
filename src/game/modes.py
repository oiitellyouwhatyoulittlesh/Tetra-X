"""
Tetra-X

File:
    modes.py

Purpose:
    Defines the available Tetra-X game modes.
"""

from enum import Enum


class GameMode(Enum):
    """
    Available Tetra-X game modes.
    """

    ZEN = "ZEN"
    BLITZ = "BLITZ"
    FORTY_LINES = "40 LINES"
