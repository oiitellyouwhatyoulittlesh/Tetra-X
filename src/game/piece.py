"""
Tetra-X

File:
    piece.py

Purpose:
    Represents the current falling piece.

"""

from utils.vector import Vector2
from game.pieces import (
    get_cells,
    get_colour,
    get_spawn
)


class Piece:
    """
    Represents the current falling piece.
    """

    def __init__(self, piece: str) -> None:

        self.type = piece
        self.rotation = 0

        spawn_x, spawn_y = get_spawn(piece)
        self.position = Vector2(spawn_x, spawn_y)

    # ====================
    # Position
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
        Returns the piece colour.
        """

        return get_colour(self.type)

    def move(self, dx: int, dy: int) -> None:
        """
        Moves the piece.
        """

        self.position.move(dx, dy)

    def set_position(self, x: int, y: int) -> None:
        """
        Sets the piece position.
        """

        self.position.set(x, y)

    # ====================
    # Rotation
    # ====================

    def rotate_cw(self) -> None:
        """
        Rotates clockwise.
        """

        self.rotation = (self.rotation + 1) % 4

    def rotate_ccw(self) -> None:
        """
        Rotates counter-clockwise.
        """

        self.rotation = (self.rotation - 1) % 4

    def rotate_180(self) -> None:
        """
        Rotates 180 degrees.
        """

        self.rotation = (self.rotation + 2) % 4

    # ====================
    # Information
    # ====================

    def get_cells(self) -> list[tuple[int, int]]:
        """
        Returns the piece's cells in board coordinates.
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
        Moves the piece back to its spawn position.
        """

        self.rotation = 0

        spawn_x, spawn_y = get_spawn(self.type)
        self.position.set(spawn_x, spawn_y)

    def copy(self) -> "Piece":
        """
        Returns a copy of this piece.
        """

        piece = Piece(self.type)

        piece.rotation = self.rotation
        piece.position = self.position.copy()

        return piece

    # ====================
    # String
    # ====================

    def __repr__(self) -> str:

        return (
            f"Piece("
            f"type='{self.type}', "
            f"rotation={self.rotation}, "
            f"position={self.position}"
            f")"
        )
