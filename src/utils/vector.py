"""
Tetra-X

File:
    vector.py

Purpose:
    Represents a 2D integer position.

"""


class Vector2:
    """
    Represents a 2D integer vector.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:

        self.x = x
        self.y = y

    # ====================
    # Basic Operations
    # ====================

    def set(self, x: int, y: int) -> None:
        """
        Sets the vector.
        """

        self.x = x
        self.y = y

    def move(self, dx: int, dy: int) -> None:
        """
        Moves the vector.
        """

        self.x += dx
        self.y += dy

    def copy(self) -> "Vector2":
        """
        Returns a copy of this vector.
        """

        return Vector2(self.x, self.y)
