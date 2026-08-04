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
        (-1, -1),
        (0, 2),
        (-1, 2)
    ],

    "1->0": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, -2),
        (1, -2)
    ],

    "1->2": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, -2),
        (1, -2)
    ],

    "2->1": [
        (0, 0),
        (-1, 0),
        (-1, -1),
        (0, 2),
        (-1, 2)
    ],

    "2->3": [
        (0, 0),
        (1, 0),
        (1, -1),
        (0, 2),
        (1, 2)
    ],

    "3->2": [
        (0, 0),
        (-1, 0),
        (-1, 1),
        (0, -2),
        (-1, -2)
    ],

    "3->0": [
        (0, 0),
        (-1, 0),
        (-1, 1),
        (0, -2),
        (-1, -2)
    ],

    "0->3": [
        (0, 0),
        (1, 0),
        (1, -1),
        (0, 2),
        (1, 2)
    ]
}


# ====================
# I Piece Kick Data
# ====================

I_KICKS = {

    "0->1": [
        (0, 0),
        (-2, 0),
        (1, 0),
        (-2, 1),
        (1, -2)
    ],

    "1->0": [
        (0, 0),
        (2, 0),
        (-1, 0),
        (2, -1),
        (-1, 2)
    ],

    "1->2": [
        (0, 0),
        (-1, 0),
        (2, 0),
        (-1, -2),
        (2, 1)
    ],

    "2->1": [
        (0, 0),
        (1, 0),
        (-2, 0),
        (1, 2),
        (-2, -1)
    ],

    "2->3": [
        (0, 0),
        (2, 0),
        (-1, 0),
        (2, -1),
        (-1, 2)
    ],

    "3->2": [
        (0, 0),
        (-2, 0),
        (1, 0),
        (-2, 1),
        (1, -2)
    ],

    "3->0": [
        (0, 0),
        (1, 0),
        (-2, 0),
        (1, 2),
        (-2, -1)
    ],

    "0->3": [
        (0, 0),
        (-1, 0),
        (2, 0),
        (-1, -2),
        (2, 1)
    ]
}


# ====================
# 180 Degree Kicks
# ====================

KICKS_180 = {

    "0->2": [
        (0, 0),
        (0, -1),
        (1, -1),
        (-1, -1),
        (1, 0),
        (-1, 0)
    ],

    "2->0": [
        (0, 0),
        (0, 1),
        (-1, 1),
        (1, 1),
        (-1, 0),
        (1, 0)
    ],

    "1->3": [
        (0, 0),
        (1, 0),
        (1, 2),
        (1, -1),
        (2, 0),
        (-1, 0)
    ],

    "3->1": [
        (0, 0),
        (-1, 0),
        (-1, 2),
        (-1, -1),
        (-2, 0),
        (1, 0)
    ]
}


# ====================
# Rotation System
# ====================

class Rotation:
    """
    Handles piece rotation and wall kicks.
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

    def rotate_cw(
        self,
        piece
    ) -> bool:
        """
        Attempts clockwise rotation.
        """

        return self._rotate(
            piece,
            1
        )


    def rotate_ccw(
        self,
        piece
    ) -> bool:
        """
        Attempts counter clockwise rotation.
        """

        return self._rotate(
            piece,
            -1
        )


    def rotate_180(
        self,
        piece
    ) -> bool:
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

    def _rotate(
        self,
        piece,
        amount: int
    ) -> bool:
        """
        Attempts a rotation and applies wall kicks.

        The piece is returned to its exact original
        rotation and position if every kick fails.
        """

        old_rotation = piece.rotation

        new_rotation = (
            old_rotation + amount
        ) % 4


        kick_data = self.get_kicks(
            piece,
            old_rotation,
            new_rotation,
            amount
        )


        if not kick_data:
            return False


        # Apply the new rotation once.
        piece.rotation = new_rotation


        # Test every kick.
        for dx, dy in kick_data:

            piece.move(
                dx,
                dy
            )


            if self.collision.valid_position(
                piece
            ):

                # Rotation succeeded.
                # Keep the new rotation and position.
                return True


            # Failed kick.
            # Undo only the position change.
            piece.move(
                -dx,
                -dy
            )


        # Every kick failed.
        # Restore the original rotation.
        piece.rotation = old_rotation


        return False


    # ====================
    # Kick Selection
    # ====================

    def get_kicks(
        self,
        piece,
        old_rotation: int,
        new_rotation: int,
        amount: int
    ):
        """
        Returns the correct kick table.
        """

        transition = (
            f"{old_rotation}->{new_rotation}"
        )


        # 180 degree rotation.
        if abs(amount) == 2:

            return KICKS_180.get(
                transition,
                []
            )


        # I piece.
        if piece.type == "I":

            return I_KICKS.get(
                transition,
                []
            )


        # J, L, S, T and Z.
        return NORMAL_KICKS.get(
            transition,
            []
        )
