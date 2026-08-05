"""
Tetra-X

File:
    pause_menu.py

Purpose:
    Displays and handles the pause menu.
"""

import pygame

from screens.screen import Screen


class PauseMenu(Screen):
    """
    Pause menu screen.
    """

    def __init__(
        self,
        screen_manager,
        game_screen
    ) -> None:

        self.screen_manager = screen_manager
        self.game_screen = game_screen

        self.options = [
            "RESUME",
            "SETTINGS",
            "QUIT TO MENU"
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


            if event.key == pygame.K_UP:

                self.selected = (
                    self.selected - 1
                ) % len(self.options)


            elif event.key == pygame.K_DOWN:

                self.selected = (
                    self.selected + 1
                ) % len(self.options)


            elif event.key == pygame.K_ESCAPE:

                self.resume()


            elif event.key == pygame.K_RETURN:

                self.select()


    # ====================
    # Selection
    # ====================

    def select(self) -> None:
        """
        Handles the selected option.
        """

        option = self.options[
            self.selected
        ]


        if option == "RESUME":

            self.resume()


        elif option == "SETTINGS":

            print(
                "SETTINGS NOT IMPLEMENTED YET"
            )


        elif option == "QUIT TO MENU":

            from screens.main_menu import MainMenu

            self.screen_manager.set_screen(
                MainMenu(
                    self.screen_manager
                )
            )


    def resume(self) -> None:
        """
        Returns to the active game.
        """

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

        pass


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
