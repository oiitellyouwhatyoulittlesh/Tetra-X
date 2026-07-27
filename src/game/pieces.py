"""
Tetra-X

File:
    pieces.py

Purpose:
    Stores the data for every game piece.

"""

from constants import (
    PIECE_I,
    PIECE_O,
    PIECE_T,
    PIECE_S,
    PIECE_Z,
    PIECE_J,
    PIECE_L
)

# ====================
# Piece Data
# ====================

PIECES = {

    "I": {
        "colour": PIECE_I,
        "spawn": (3, 18),
        "rotations": [

            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 0), (1, 1), (1, 2), (1, 3)]

        ]
    },

    "O": {
        "colour": PIECE_O,
        "spawn": (4, 18),
        "rotations": [

            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)]

        ]
    },

    "T": {
        "colour": PIECE_T,
        "spawn": (3, 18),
        "rotations": [

            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)]

        ]
    },

    "S": {
        "colour": PIECE_S,
        "spawn": (3, 18),
        "rotations": [

            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]

        ]
    },

    "Z": {
        "colour": PIECE_Z,
        "spawn": (3, 18),
        "rotations": [

            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (0, 1), (1, 1), (0, 2)]

        ]
    },

    "J": {
        "colour": PIECE_J,
        "spawn": (3, 18),
        "rotations": [

            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)]

        ]
    },

    "L": {
        "colour": PIECE_L,
        "spawn": (3, 18),
        "rotations": [

            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)]

        ]
    }

}

# ====================
# Helper Functions
# ====================

def get_cells(piece: str, rotation: int) -> list[tuple[int, int]]:
    """
    Returns the cell positions for a piece.
    """

    return PIECES[piece]["rotations"][rotation]


def get_colour(piece: str) -> tuple[int, int, int]:
    """
    Returns the colour of a piece.
    """

    return PIECES[piece]["colour"]


def get_spawn(piece: str) -> tuple[int, int]:
    """
    Returns the spawn position of a piece.
    """

    return PIECES[piece]["spawn"]
