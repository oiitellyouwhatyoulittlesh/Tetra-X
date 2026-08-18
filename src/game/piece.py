"""
Tetra-X

File:
    piece.py

Purpose:
    Represents the current active falling piece.
"""

from game.pieces import (
    get_cells,
    get_colour,
    get_spawn,
)
from utils.vector import Vector2


class Piece:
    """
    Represents the current active falling piece.
    """

    def __init__(self, piece: str) -> None:
        self.type = piece
        self.rotation = 0

        spawn_x, spawn_y = get_spawn(piece)
        self.position = Vector2(spawn_x, spawn_y)


    # ====================
    # Position & Properties
    # ====================

    @property
    def x(self) -> int:
        return self.position.x


    @property
    def y(self) -> int:
        return self.position.y


    @property
    def colour(self) -> tuple[int, int, int]:
        """
        Returns the piece colour tuple.
        """
        return get_colour(self.type)


    def move(self, dx: int, dy: int) -> None:
        """
        Moves the piece by the specified offsets.
        """
        self.position.move(dx, dy)


    def set_position(self, x: int, y: int) -> None:
        """
        Sets the piece position directly.
        """
        self.position.set(x, y)


    # ====================
    # Rotation
    # ====================

    def rotate_cw(self) -> None:
        """
        Rotates state clockwise.
        """
        self.rotation = (self.rotation + 1) % 4


    def rotate_ccw(self) -> None:
        """
        Rotates state counter-clockwise.
        """
        self.rotation = (self.rotation - 1) % 4


    def rotate_180(self) -> None:
        """
        Rotates state 180 degrees.
        """
        self.rotation = (self.rotation + 2) % 4


    # ====================
    # Information & Utility
    # ====================

    def get_cells(self) -> list[tuple[int, int]]:
        """
        Returns the piece's cell positions in playfield board coordinates.
        """
        cells = []

        for x, y in get_cells(self.type, self.rotation):
            cells.append((
                self.x + x,
                self.y + y
            ))

        return cells


    def reset(self) -> None:
        """
        Resets the piece orientation and moves it back to its spawn position.
        """
        self.rotation = 0

        spawn_x, spawn_y = get_spawn(self.type)
        self.position.set(spawn_x, spawn_y)


    def copy(self) -> "Piece":
        """
        Returns an exact copy of this piece instance.
        """
        piece = Piece(self.type)
        piece.rotation = self.rotation
        piece.position = self.position.copy()

        return piece


    # ====================
    # Representation
    # ====================

    def __repr__(self) -> str:
        return (
            f"Piece("
            f"type='{self.type}', "
            f"rotation={self.rotation}, "
            f"position={self.position}"
            f")"
        )
