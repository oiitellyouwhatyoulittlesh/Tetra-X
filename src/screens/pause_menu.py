"""
Tetra-X

File:
    pause_menu.py

Purpose:
    Displays and handles the pause menu.
"""

from screens.screen import Screen

from input.controls import Controls


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

        self.screen_manager = screen_manager
        self.game_screen = game_screen
        self.settings = settings

        self.controls = Controls(
            settings
        )

        self.options = [
            "RESUME",
            "RESTART",
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
        """
        Handles pause menu input.
        """

        actions = self.controls.get_event_actions(
            events
        )


        for action in actions:

            if action == "menu_up":

                self.selected = (
                    self.selected - 1
                ) % len(self.options)


            elif action == "menu_down":

                self.selected = (
                    self.selected + 1
                ) % len(self.options)


            elif action == "menu_back":

                self.resume()


            elif action == "menu_confirm":

                self.select()


            elif action == "restart":

                self.restart()


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
        Returns to the active game without resetting state.
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
