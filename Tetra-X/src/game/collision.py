"""
Tetra-X

File:
    collision.py

Purpose:
    Handles collision checks for the board.

"""

from constants import (
    BOARD_COLUMNS,
    BOARD_ROWS,
)


class Collision:
    """
    Handles collision checks.
    """

    def __init__(self, board) -> None:

        self.board = board

    # ====================
    # Cell Checks
    # ====================

    def inside_board(
        self,
        x: int,
        y: int
    ) -> bool:
        """
        Returns True if a position is inside the board.
        """

        return (
            0 <= x < BOARD_COLUMNS and
            y < BOARD_ROWS
        )


    def cell_empty(
        self,
        x: int,
        y: int
    ) -> bool:
        """
        Returns True if a cell is empty.
        """

        # Cells above the visible board are allowed
        if y < 0:
            return True

        return self.board.grid[y][x] is None


    # ====================
    # Piece Checks
    # ====================

    def valid_position(
        self,
        piece
    ) -> bool:
        """
        Returns True if a piece can exist at its position.
        """

        for x, y in piece.get_cells():

            if not self.inside_board(
                x,
                y
            ):
                return False

            if not self.cell_empty(
                x,
                y
            ):
                return False

        return True


    def can_move(
        self,
        piece,
        dx: int,
        dy: int
    ) -> bool:
        """
        Returns True if a piece can move.
        """

        test_piece = piece.copy()

        test_piece.move(
            dx,
            dy
        )

        return self.valid_position(
            test_piece
        )


    def is_immobile(
        self,
        piece
    ) -> bool:
        """
        Returns True if the piece cannot move upward.

        This is the simplified immobile check used
        for All-Mini+ spin detection.
        """

        return not self.can_move(
            piece,
            0,
            -1
        )


    # ====================
    # T-Spin
    # ====================

    def count_t_spin_corners(
        self,
        piece
    ) -> int:
        """
        Counts occupied or out-of-bounds corners
        around a T piece.

        Returns a value from 0 to 4.
        """

        if piece.type != "T":
            return 0

        corners = (
            (piece.x, piece.y),
            (piece.x + 2, piece.y),
            (piece.x, piece.y + 2),
            (piece.x + 2, piece.y + 2)
        )

        occupied = 0

        for x, y in corners:

            if (
                x < 0
                or x >= BOARD_COLUMNS
                or y >= BOARD_ROWS
            ):
                occupied += 1
                continue

            if y < 0:
                continue

            if self.board.grid[y][x] is not None:
                occupied += 1

        return occupied
