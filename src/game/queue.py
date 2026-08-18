"""
Tetra-X

File:
    queue.py

Purpose:
    Manages the piece queue and preview pieces.

"""

from game.bag import Bag
from game.piece import Piece


class Queue:
    """
    Represents the game's piece queue.
    """

    PREVIEW_LENGTH = 5

    def __init__(self) -> None:

        self.bag = Bag()

        self.preview = []

        self._fill_preview()

    # ====================
    # Queue
    # ====================

    def _fill_preview(self) -> None:
        """
        Fills the preview queue.
        """

        while len(self.preview) < self.PREVIEW_LENGTH:

            self.preview.append(
                self.bag.next_piece()
            )

    def take(self) -> Piece:
        """
        Removes and creates the next piece.
        """

        piece_type = self.preview.pop(0)

        self._fill_preview()

        return Piece(piece_type)

    # ====================
    # Information
    # ====================

    def get_preview(self) -> list[str]:
        """
        Returns a copy of the preview queue.
        """

        return self.preview.copy()

    def reset(self) -> None:
        """
        Resets the queue.
        """

        self.bag.reset()

        self.preview.clear()

        self._fill_preview()
