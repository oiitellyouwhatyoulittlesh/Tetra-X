"""
Tetra-X

File:
    rotation.py

Purpose:
    Handles piece rotation and wall kicks.

"""

from game.collision import Collision


# ====================
# SRS Kick Data
# ====================

NORMAL_KICKS = {

    "0->1": [
        (0, 0),
        (-1, 0),
        (-1, 1),
        (0, -2),
        (-1, -2)
    ],

    "1->0": [
        (0, 0),
        (1, 0),
        (1, -1),
        (0, 2),
        (1, 2)
    ],

    "1->2": [
        (0, 0),
        (1, 0),
        (1, -1),
        (0, 2),
        (1, 2)
    ],

    "2->1": [
        (0, 0),
        (-1, 0),
        (-1, 1),
        (0, -2),
        (-1, -2)
    ],

    "2->3": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, -2),
        (1, -2)
    ],

    "3->2": [
        (0, 0),
        (-1, 0),
        (-1, -1),
        (0, 2),
        (-1, 2)
    ],

    "3->0": [
        (0, 0),
        (-1, 0),
        (-1, -1),
        (0, 2),
        (-1, 2)
    ],

    "0->3": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, -2),
        (1, -2)
    ]
}


I_KICKS = {

    "0->1": [
        (0, 0),
        (-2, 0),
        (1, 0),
        (-2, -1),
        (1, 2)
    ],

    "1->0": [
        (0, 0),
        (2, 0),
        (-1, 0),
        (2, 1),
        (-1, -2)
    ],

    "1->2": [
        (0, 0),
        (-1, 0),
        (2, 0),
        (-1, 2),
        (2, -1)
    ],

    "2->1": [
        (0, 0),
        (1, 0),
        (-2, 0),
        (1, -2),
        (-2, 1)
    ],

    "2->3": [
        (0, 0),
        (2, 0),
        (-1, 0),
        (2, 1),
        (-1, -2)
    ],

    "3->2": [
        (0, 0),
        (-2, 0),
        (1, 0),
        (-2, -1),
        (1, 2)
    ],

    "3->0": [
        (0, 0),
        (1, 0),
        (-2, 0),
        (1, -2),
        (-2, 1)
    ],

    "0->3": [
        (0, 0),
        (-1, 0),
        (2, 0),
        (-1, 2),
        (2, -1)
    ]
}


# ====================
# Rotation System
# ====================

class Rotation:
    """
    Handles piece rotation.
    """

    def __init__(
        self,
        collision: Collision,
        board
    ):

        self.collision = collision
        self.board = board

    # ====================
    # Rotation
    # ====================

    def rotate_cw(self, piece) -> bool:
        """
        Attempts clockwise rotation.
        """

        return self._rotate(
            piece,
            1
        )

    def rotate_ccw(self, piece) -> bool:
        """
        Attempts counter clockwise rotation.
        """

        return self._rotate(
            piece,
            -1
        )

    def rotate_180(self, piece) -> bool:
        """
        Attempts 180 degree rotation.
        """

        return self._rotate(
            piece,
            2
        )

    # ====================
    # Internal
    # ====================

    def _rotate(self, piece, amount: int) -> bool:
        """
        Attempts a rotation and applies kicks.
        """

        old_rotation = piece.rotation

        new_rotation = (
            old_rotation + amount
        ) % 4


        piece.rotation = new_rotation


        if self.collision.valid_position(
            piece
        ):
            return True


        kick_data = self.get_kicks(
            piece,
            old_rotation,
            new_rotation
        )


        for dx, dy in kick_data:

            piece.move(
                dx,
                dy
            )

            if self.collision.valid_position(
                piece
            ):
                return True

            piece.move(
                -dx,
                -dy
            )


        piece.rotation = old_rotation

        return False

    def get_kicks(
        self,
        piece,
        old_rotation: int,
        new_rotation: int
    ):
        """
        Returns the correct kick table.
        """

        transition = (
            f"{old_rotation}->{new_rotation}"
        )


        if piece.type == "I":

            return I_KICKS.get(
                transition,
                []
            )


        return NORMAL_KICKS.get(
            transition,
            []
        )
