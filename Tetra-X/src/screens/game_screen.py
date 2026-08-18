"""
Tetra-X

File:
game_screen.py

Purpose:
Provides the gameplay screen.
"""

from game.game import Game
from game.modes import GameMode
from screens.pause_menu import PauseMenu
from screens.screen import Screen


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

        self.events = []

        # ====================
        # Pause
        # ====================

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

            return

        # ====================
        # Results
        # ====================

        if (
            self.game.game_over
            and self.mode in (
                GameMode.BLITZ,
                GameMode.FORTY_LINES
            )
        ):

            from screens.results_screen import ResultsScreen

            topped_out = (
                not self.game.completed
                and self.game.results == {}
            )

            if topped_out:

                results = self.game.create_results()

                new_record = False

                record_difference = 0

            else:

                results = self.game.results

                new_record = self.game.new_record

                record_difference = (
                    self.game.record_difference
                )

            self.screen_manager.set_screen(
                ResultsScreen(
                    self.screen_manager,
                    self.game.settings,
                    self.mode,
                    results,
                    new_record,
                    record_difference,
                    topped_out
                )
            )

            return

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
