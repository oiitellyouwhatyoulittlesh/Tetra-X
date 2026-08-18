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
    # Queue Management
    # ====================

    def _fill_preview(self) -> None:
        """
        Fills the preview queue up to the defined preview length.
        """
        while len(self.preview) < self.PREVIEW_LENGTH:
            self.preview.append(
                self.bag.next_piece()
            )


    def take(self) -> Piece:
        """
        Removes the next piece type from the preview queue and returns a new Piece instance.
        """
        piece_type = self.preview.pop(0)
        self._fill_preview()

        return Piece(piece_type)


    # ====================
    # Information & Utility
    # ====================

    def get_preview(self) -> list[str]:
        """
        Returns a copy of the current preview queue list.
        """
        return self.preview.copy()


    def reset(self) -> None:
        """
        Resets the piece bag and clears/refills the preview queue.
        """
        self.bag.reset()
        self.preview.clear()
        self._fill_preview()
