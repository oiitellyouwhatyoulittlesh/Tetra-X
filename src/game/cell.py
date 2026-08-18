"""
Tetra-X

File:
    cell.py

Purpose:
    Represents one occupied cell on the board.
"""

from utils.vector import Vector2


class Cell:
    """
    Represents one occupied cell.
    """

    def __init__(self, x: int, y: int, colour: tuple[int, int, int]) -> None:
        self.position = Vector2(x, y)
        self.colour = colour


    # ====================
    # Position Properties & Movement
    # ====================

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def set_position(self, x: int, y: int) -> None:
        """
        Sets the cell position directly.
        """
        self.position.set(x, y)

    def move(self, dx: int, dy: int) -> None:
        """
        Moves the cell position by offsets.
        """
        self.position.move(dx, dy)

    def copy(self) -> "Cell":
        """
        Returns a duplicate copy of this cell.
        """
        return Cell(
            self.x,
            self.y,
            self.colour
        )


    # ====================
    # Representation
    # ====================

    def __repr__(self) -> str:
        return f"Cell(x={self.x}, y={self.y})"
