"""
Tetra-X

File:
    vector.py

Purpose:
    Represents a 2D integer position or offset vector.
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
        Sets the vector coordinates.
        """
        self.x = x
        self.y = y


    def move(self, dx: int, dy: int) -> None:
        """
        Offsets the vector coordinates by dx and dy.
        """
        self.x += dx
        self.y += dy


    def copy(self) -> "Vector2":
        """
        Returns a new Vector2 copy of this instance.
        """
        return Vector2(self.x, self.y)


    # ====================
    # Operators
    # ====================

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(
            self.x + other.x,
            self.y + other.y
        )


    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(
            self.x - other.x,
            self.y - other.y
        )


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return False

        return self.x == other.x and self.y == other.y


    # ====================
    # Representation
    # ====================

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
