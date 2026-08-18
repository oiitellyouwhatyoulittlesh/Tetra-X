"""
Tetra-X

File:
main_menu.py

Purpose:
Displays and handles the main menu.
"""

import pygame

from screens.screen import Screen


class MainMenu(Screen):
    """
    Main menu screen.
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
            "PLAY",
            "SETTINGS",
            "QUIT"
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
        Handles the currently selected option.
        """

        option = self.options[
            self.selected
        ]

        if option == "PLAY":

            from screens.mode_select import ModeSelect

            self.screen_manager.set_screen(
                ModeSelect(
                    self.screen_manager,
                    self.settings
                )
            )

        elif option == "SETTINGS":

            from screens.settings_menu import SettingsMenu

            self.screen_manager.set_screen(
                SettingsMenu(
                    self.screen_manager,
                    self.settings
                )
            )

        elif option == "QUIT":

            pygame.event.post(
                pygame.event.Event(
                    pygame.QUIT
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
            "TETRA-X",
            self.options,
            self.selected
        )
