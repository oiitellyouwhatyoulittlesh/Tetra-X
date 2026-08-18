"""
Tetra-X

File:
    bag.py

Purpose:
    Implements the 7 bag randomiser.
"""

import random


class Bag:
    """
    Represents the game's 7 bag randomiser.
    """

    PIECES = (
        "I",
        "O",
        "T",
        "S",
        "Z",
        "J",
        "L"
    )

    def __init__(self) -> None:
        self.bag = []
        self._generate_bag()


    # ====================
    # Bag Generation
    # ====================

    def _generate_bag(self) -> None:
        """
        Creates a new shuffled 7 piece bag.
        """
        new_bag = list(self.PIECES)
        random.shuffle(new_bag)
        self.bag.extend(new_bag)


    def next_piece(self) -> str:
        """
        Returns the next piece and replenishes the bag if low.
        """
        if len(self.bag) <= 7:
            self._generate_bag()

        return self.bag.pop(0)


    # ====================
    # Information & Utility
    # ====================

    def peek(self, amount: int = 5) -> list[str]:
        """
        Returns upcoming preview pieces without removing them.
        """
        while len(self.bag) < amount:
            self._generate_bag()

        return self.bag[:amount]


    def reset(self) -> None:
        """
        Clears and regenerates the piece bag.
        """
        self.bag.clear()
        self._generate_bag()
