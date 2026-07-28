"""
Tetra-X

File:
    bag.py

Purpose:
    Implements the 7-bag randomiser.

"""

import random


class Bag:
    """
    Represents the game's 7-bag randomiser.
    """

    PIECES = [
        "I",
        "O",
        "T",
        "S",
        "Z",
        "J",
        "L"
    ]

    def __init__(self) -> None:

        self.bag = []

        self._generate_bag()

    # ====================
    # Bag
    # ====================

    def _generate_bag(self) -> None:
        """
        Creates a new shuffled bag.
        """

        new_bag = self.PIECES.copy()

        random.shuffle(new_bag)

        self.bag.extend(new_bag)

    def next_piece(self) -> str:
        """
        Returns the next piece.
        """

        if len(self.bag) <= 7:
            self._generate_bag()

        return self.bag.pop(0)

    # ====================
    # Information
    # ====================

    def peek(self, amount: int = 5) -> list[str]:
        """
        Returns the next pieces without removing them.
        """

        while len(self.bag) < amount:
            self._generate_bag()

        return self.bag[:amount]

    def reset(self) -> None:
        """
        Resets the bag.
        """

        self.bag.clear()

        self._generate_bag()
