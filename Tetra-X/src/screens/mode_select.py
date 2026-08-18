"""
Tetra-X

File:
    mode_select.py

Purpose:
    Displays and handles game mode selection.
"""

import pygame

from game.modes import GameMode
from screens.game_screen import GameScreen
from screens.screen import Screen


class ModeSelect(Screen):
    """
    Game mode selection screen.
    """

    def __init__(
        self,
        screen_manager,
        settings
    ) -> None:

        super().__init__(
            settings
        )

        self.screen_manager = screen_manager

        self.options = [
            "ZEN",
            "BLITZ",
            "40 LINES",
            "BACK"
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

        for event in events:

            if event.type == pygame.KEYDOWN:

                # ====================
                # Menu Up
                # ====================

                if event.key == self.settings.controls.menu_up:

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

                elif event.key == self.settings.controls.menu_down:

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

                elif event.key == self.settings.controls.menu_back:

                    self.go_back()

                # ====================
                # Menu Confirm
                # ====================

                elif event.key == self.settings.controls.menu_confirm:

                    self.select()

            elif event.type == pygame.KEYUP:

                # ====================
                # Stop Navigation
                # ====================

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
        Handles the selected game mode.
        """

        option = self.options[
            self.selected
        ]


        if option == "ZEN":

            self.start_game(
                GameMode.ZEN
            )


        elif option == "BLITZ":

            self.start_game(
                GameMode.BLITZ
            )


        elif option == "40 LINES":

            self.start_game(
                GameMode.FORTY_LINES
            )


        elif option == "BACK":

            self.go_back()


    def go_back(self) -> None:
        """
        Returns to the main menu.
        """

        from screens.main_menu import MainMenu

        self.screen_manager.set_screen(
            MainMenu(
                self.screen_manager,
                self.settings
            )
        )


    def start_game(
        self,
        mode: GameMode
    ) -> None:
        """
        Starts a game using the selected mode.
        """

        self.screen_manager.set_screen(
            GameScreen(
                self.screen_manager,
                mode
            )
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
            "SELECT MODE",
            self.options,
            self.selected
        )
