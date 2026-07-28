"""
Tetra-X

File:
    board.py

Purpose:
    Handles the Tetris playfield and game logic.

"""

from constants import (
    BOARD_COLUMNS,
    BOARD_ROWS
)

from game.queue import Queue
from game.piece import Piece
from game.collision import Collision
from game.rotation import Rotation


class Board:
    """
    Represents the game board.
    """


    def __init__(self) -> None:

        self.grid = self.create_grid()

        self.queue = Queue()

        self.collision = Collision(
            self
        )

        self.rotation = Rotation(
            self.collision,
            self
        )

        self.current_piece: Piece | None = None

        self.lines = 0
        self.score = 0

        self.spawn_piece()


    # ====================
    # Grid
    # ====================

    def create_grid(self) -> list[list]:

        """
        Creates an empty board.
        """

        return [
            [
                None
                for _ in range(BOARD_COLUMNS)
            ]
            for _ in range(BOARD_ROWS)
        ]


    # ====================
    # Pieces
    # ====================

    def spawn_piece(self) -> bool:
        """
        Spawns the next piece.

        Returns False if the player tops out.
        """

        self.current_piece = (
            self.queue.take()
        )


        if not self.collision.valid_position(
            self.current_piece
        ):

            return False


        return True


    def lock_piece(self) -> None:
        """
        Places the current piece into the board.
        """

        if self.current_piece is None:
            return
        
        for x, y in self.current_piece.get_cells():

            if y >= 0:

                self.grid[y][x] = (
                    self.current_piece.colour
                )


    # ====================
    # Movement
    # ====================

    def move_piece(
        self,
        dx: int,
        dy: int
    ) -> bool:
        """
        Attempts to move the piece.
        """

        if self.current_piece is None:
            return False

        if self.collision.can_move(
            self.current_piece,
            dx,
            dy
        ):

            self.current_piece.move(
                dx,
                dy
            )

            return True


        return False



    def rotate_cw(self) -> bool:
        """
        Rotates clockwise.
        """

        if self.current_piece is None:
            return False
        
        return self.rotation.rotate_cw(
            self.current_piece
        )


    def rotate_ccw(self) -> bool:
        """
        Rotates counter-clockwise.
        """

        if self.current_piece is None:
            return False

        return self.rotation.rotate_ccw(
            self.current_piece
        )


    def rotate_180(self) -> bool:
        """
        Rotates 180 degrees.
        """

        if self.current_piece is None:
            return False
        
        return self.rotation.rotate_180(
            self.current_piece
        )


    # ====================
    # Lines
    # ====================

    def clear_lines(self) -> int:
        """
        Removes completed lines.
        """

        cleared = 0


        new_grid = []


        for row in self.grid:

            if all(cell is not None for cell in row):

                cleared += 1

            else:

                new_grid.append(row)


        while len(new_grid) < BOARD_ROWS:

            new_grid.insert(
                0,
                [
                    None
                    for _ in range(BOARD_COLUMNS)
                ]
            )


        self.grid = new_grid

        self.lines += cleared

        return cleared


    # ====================
    # Information
    # ====================

    def get_preview(self) -> list[str]:
        """
        Returns upcoming pieces.
        """

        return self.queue.get_preview()


    def reset(self) -> None:
        """
        Resets the board.
        """

        self.grid = self.create_grid()

        self.queue.reset()

        self.lines = 0
        self.score = 0

        self.spawn_piece()
