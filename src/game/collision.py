"""
Tetra-X

File:
    collision.py

Purpose:
    Handles collision checks for the board.

"""


from constants import (
    BOARD_COLUMNS,
    BOARD_ROWS
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
