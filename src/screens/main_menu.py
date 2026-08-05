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
    # Input
    # ====================

    def handle_events(
        self,
        events
    ) -> None:

        for event in events:

            if event.type != pygame.KEYDOWN:
                continue


            if event.key == self.settings.controls.menu_up:

                self.selected = (
                    self.selected - 1
                ) % len(self.options)


            elif event.key == self.settings.controls.menu_down:

                self.selected = (
                    self.selected + 1
                ) % len(self.options)


            elif event.key == self.settings.controls.menu_confirm:

                self.select()


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

        pass


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
