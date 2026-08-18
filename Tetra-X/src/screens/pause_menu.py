"""
Tetra-X

File:
    pause_menu.py

Purpose:
    Displays and handles the pause menu.
"""

import pygame

from game.modes import GameMode
from input.controls import Controls
from screens.screen import Screen


class PauseMenu(Screen):
    """
    Pause menu screen.
    """

    def __init__(
        self,
        screen_manager,
        game_screen,
        settings
    ) -> None:

        super().__init__(
            settings
        )

        self.screen_manager = screen_manager
        self.game_screen = game_screen
        self.settings = settings

        self.controls = Controls(
            settings
        )

        # ====================
        # Menu Options
        # ====================

        if self.game_screen.game.mode == GameMode.ZEN:

            self.options = [
                "RESUME",
                "RESTART",
                "QUIT TO MENU"
            ]

        else:

            self.options = [
                "RESTART",
                "QUIT TO MENU"
            ]

        self.selected = 0

        # ====================
        # Navigation
        # ====================

        self.navigation_timer = 0.0
        self.navigation_direction = 0

        self.navigation_initial_delay = 0.30
        self.navigation_repeat_delay = 0.08

    # ====================
    # Input
    # ====================

    def handle_events(
        self,
        events
    ) -> None:
        """
        Handles pause menu input.
        """

        actions = self.controls.get_event_actions(
            events
        )

        for action in actions:

            # ====================
            # Menu Up
            # ====================

            if action == "menu_up":

                self.selected = (
                    self.selected - 1
                ) % len(self.options)

                self.navigation_direction = -1
                self.navigation_timer = (
                    -self.navigation_initial_delay
                )

            # ====================
            # Menu Down
            # ====================

            elif action == "menu_down":

                self.selected = (
                    self.selected + 1
                ) % len(self.options)

                self.navigation_direction = 1
                self.navigation_timer = (
                    -self.navigation_initial_delay
                )

            # ====================
            # Menu Back
            # ====================

            elif action == "menu_back":

                if self.game_screen.game.mode == GameMode.ZEN:

                    self.resume()

            # ====================
            # Menu Confirm
            # ====================

            elif action == "menu_confirm":

                self.select()

            # ====================
            # Restart
            # ====================

            elif action == "restart":

                self.restart()

        # ====================
        # Stop Navigation
        # ====================

        for event in events:

            if event.type != pygame.KEYUP:
                continue

            stop_conditions = {
                self.settings.controls.menu_up: -1,
                self.settings.controls.menu_down: 1,
            }

            if stop_conditions.get(event.key) == self.navigation_direction:
                self.navigation_direction = 0

    # ====================
    # Selection
    # ====================

    def select(self) -> None:
        """
        Handles the selected pause-menu option.
        """

        option = self.options[
            self.selected
        ]

        if option == "RESUME":

            self.resume()

        elif option == "RESTART":

            self.restart()

        elif option == "QUIT TO MENU":

            from screens.main_menu import MainMenu

            self.screen_manager.set_screen(
                MainMenu(
                    self.screen_manager,
                    self.settings
                )
            )

    # ====================
    # Resume
    # ====================

    def resume(self) -> None:
        """
        Returns to the active game without
        resetting state.
        """

        self.game_screen.game.paused = False

        self.game_screen.events = []

        self.game_screen.game.input.reset_handling()

        self.screen_manager.set_screen(
            self.game_screen
        )

    # ====================
    # Restart
    # ====================

    def restart(self) -> None:
        """
        Restarts the current game.
        """

        self.game_screen.game.restart()

        self.game_screen.events = []

        self.screen_manager.set_screen(
            self.game_screen
        )

    # ====================
    # Update
    # ====================

    def update(
        self,
        delta_time: float
    ) -> None:
        """
        Handles held menu navigation.
        """

        if self.navigation_direction == 0:

            return

        self.navigation_timer += delta_time

        if self.navigation_timer < 0:

            return

        while (
            self.navigation_timer
            >= self.navigation_repeat_delay
        ):

            self.navigation_timer -= (
                self.navigation_repeat_delay
            )

            self.selected = (
                self.selected
                + self.navigation_direction
            ) % len(self.options)

    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        renderer
    ) -> None:

        renderer.draw_menu(
            "PAUSED",
            self.options,
            self.selected
        )
