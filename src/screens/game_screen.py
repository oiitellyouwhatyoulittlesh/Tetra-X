"""
Tetra-X

File:
    game_screen.py

Purpose:
    Provides the gameplay screen.
"""

from screens.screen import Screen
from screens.pause_menu import PauseMenu

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

        was_paused = self.game.paused

        self.game.update(
            delta_time,
            self.events
        )

        # Clear events so they don't leak into subsequent frames
        self.events = []

        if (
            not was_paused
            and self.game.paused
        ):

            self.screen_manager.set_screen(
                PauseMenu(
                    self.screen_manager,
                    self,
                    self.game.settings
                )
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
            self.game
        )
