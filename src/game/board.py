"""
Tetra-X

File:
    board.py

Purpose:
    Handles the game playfield and game logic.
"""

from constants import BOARD_COLUMNS, BOARD_ROWS
from game.collision import Collision
from game.piece import Piece
from game.queue import Queue
from game.rotation import Rotation


class Board:
    """
    Represents the game board.
    """

    def __init__(self) -> None:
        self.grid = self.create_grid()
        self.queue = Queue()

        self.collision = Collision(self)
        self.rotation = Rotation(self.collision, self)

        self.current_piece: Piece | None = None
        self.held_piece: str | None = None
        self.can_hold = True

        self.lines = 0
        self.score = 0

        self.spawn_piece()


    # ====================
    # Grid
    # ====================

    def create_grid(self) -> list[list]:
        """
        Creates an empty playfield grid.
        """
        return [
            [None for _ in range(BOARD_COLUMNS)]
            for _ in range(BOARD_ROWS)
        ]


    def is_all_clear(self) -> bool:
        """
        Returns True if the playfield is completely empty.
        """
        return all(
            cell is None
            for row in self.grid
            for cell in row
        )


    # ====================
    # Piece Management
    # ====================

    def spawn_piece(self) -> bool:
        """
        Spawns the next piece from the queue.

        Returns False if the spawned piece collides immediately (top out).
        """
        self.current_piece = self.queue.take()
        return self.collision.valid_position(self.current_piece)


    def hold(self) -> bool:
        """
        Holds or swaps the current piece.
        """
        if self.current_piece is None or not self.can_hold:
            return False

        self.can_hold = False

        if self.held_piece is None:
            self.held_piece = self.current_piece.type
            return self.spawn_piece()

        current = self.current_piece.type
        self.current_piece = Piece(self.held_piece)
        self.current_piece.reset()
        self.held_piece = current

        return True


    def lock_piece(self) -> None:
        """
        Places the current active piece permanently onto the grid.
        """
        if self.current_piece is None:
            return

        for x, y in self.current_piece.get_cells():
            if y >= 0:
                self.grid[y][x] = self.current_piece.colour

        self.can_hold = True


    # ====================
    # Movement & Rotation
    # ====================

    def move_piece(self, dx: int, dy: int) -> bool:
        """
        Attempts to move the current piece by the given offsets.
        """
        if self.current_piece is None:
            return False

        if self.collision.can_move(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True

        return False


    def rotate_cw(self) -> bool:
        """
        Rotates the current piece clockwise.
        """
        if self.current_piece is None:
            return False

        return self.rotation.rotate_cw(self.current_piece)


    def rotate_ccw(self) -> bool:
        """
        Rotates the current piece counter-clockwise.
        """
        if self.current_piece is None:
            return False

        return self.rotation.rotate_ccw(self.current_piece)


    def rotate_180(self) -> bool:
        """
        Rotates the current piece 180 degrees.
        """
        if self.current_piece is None:
            return False

        return self.rotation.rotate_180(self.current_piece)


    # ====================
    # Line Clearing
    # ====================

    def clear_lines(self) -> int:
        """
        Removes full rows from the grid and shifts higher rows down.
        """
        cleared = 0
        new_grid = []

        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)

        while len(new_grid) < BOARD_ROWS:
            new_grid.insert(0, [None for _ in range(BOARD_COLUMNS)])

        self.grid = new_grid
        self.lines += cleared

        return cleared


    # ====================
    # Information & Utility
    # ====================

    def get_preview(self) -> list[str]:
        """
        Returns upcoming queue items for display.
        """
        return self.queue.get_preview()


    def get_ghost_piece(self) -> Piece | None:
        """
        Returns a projected copy of the current piece positioned at its landing spot.
        """
        if self.current_piece is None:
            return None

        ghost = self.current_piece.copy()

        while self.collision.can_move(ghost, 0, 1):
            ghost.move(0, 1)

        return ghost


    def get_spin_type(self, was_rotation: bool) -> str | None:
        """
        Determines if the last move qualifies as a spin detection.

        Returns:
            "T-SPIN", "MINI", or None
        """
        if self.current_piece is None or not was_rotation:
            return None

        piece = self.current_piece

        # Check for T-Piece specific corner checks
        if piece.type == "T":
            corners = self.collision.count_t_spin_corners(piece)

            if corners >= 3:
                return "T-SPIN"

            if self.collision.is_immobile(piece):
                return "MINI"

            return None

        # Check for general immobile mini spins on other pieces
        if self.collision.is_immobile(piece):
            return "MINI"

        return None


    def is_t_spin(self) -> bool:
        """
        Returns True if the current piece orientation forms a T-Spin.
        """
        return self.get_spin_type(True) == "T-SPIN"


    def reset(self) -> None:
        """
        Resets the board state back to default.
        """
        self.grid = self.create_grid()
        self.queue.reset()

        self.lines = 0
        self.score = 0

        self.current_piece = None
        self.held_piece = None
        self.can_hold = True

        self.spawn_piece()
