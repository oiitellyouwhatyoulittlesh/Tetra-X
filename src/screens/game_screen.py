"""
Tetra-X

File:
    game_screen.py

Purpose:
    Provides the gameplay screen.
"""

from screens.screen import Screen

from game.game import Game
from game.modes import GameMode


class GameScreen(Screen):
    """
    Gameplay screen.
    """

    def __init__(
        self,
        screen_manager,
        mode: GameMode
    ) -> None:

        self.screen_manager = screen_manager
        self.mode = mode

        self.game = Game(
            mode
        )

        self.events = []

        self.game.start()


    # ====================
    # Input
    # ====================

    def handle_events(
        self,
        events
    ) -> None:
        """
        Stores gameplay events for the game update.
        """

        self.events = events


    # ====================
    # Update
    # ====================

    def update(
        self,
        delta_time: float
    ) -> None:
        """
        Updates the game.
        """

        self.game.update(
            delta_time,
            self.events
        )


    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        renderer
    ) -> None:
        """
        Draws the game.
        """

        renderer.clear()

        renderer.draw_board(
            self.game.get_board()
        )
