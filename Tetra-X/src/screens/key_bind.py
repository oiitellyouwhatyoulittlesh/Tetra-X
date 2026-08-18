"""
Tetra-X

File:
    key_bind.py

Purpose:
    Handles keyboard control rebinding.
"""

import pygame

from screens.screen import Screen


class Rebind(Screen):
    """
    Screen used to rebind a single keyboard action.
    """

    def __init__(
        self,
        screen_manager,
        settings,
        action: str,
        name: str,
        return_screen
    ) -> None:

        super().__init__(
            settings
        )

        self.screen_manager = screen_manager

        self.action = action
        self.name = name

        self.return_screen = return_screen

        self.error_message = ""


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


            # ====================
            # Menu Back
            # ====================

            if (
                event.key
                == self.settings.controls.menu_back
            ):

                self.go_back()

                return


            # ====================
            # Check Duplicate
            # ====================

            duplicate = self.find_duplicate(
                event.key
            )


            if duplicate is not None:

                self.error_message = (
                    "KEY ALREADY IN USE"
                )

                continue


            # ====================
            # Apply Binding
            # ====================

            if self.settings.set_control(
                self.action,
                event.key
            ):

                self.settings.save()

                self.go_back()

                return


    # ====================
    # Duplicate Detection
    # ====================

    def find_duplicate(
        self,
        key: int
    ) -> str | None:
        """
        Finds another action using the supplied key.

        Gameplay controls may share keys with menu controls,
        because they are used in different game states.

        Menu controls may share keys with gameplay controls,
        but duplicate keys within the same context are blocked.
        """

        gameplay_actions = (
            "move_left",
            "move_right",
            "soft_drop",
            "hard_drop",
            "rotate_cw",
            "rotate_ccw",
            "rotate_180",
            "hold",
            "pause",
            "restart"
        )

        menu_actions = (
            "menu_up",
            "menu_down",
            "menu_confirm",
            "menu_back"
        )


        if self.action in gameplay_actions:

            actions = gameplay_actions

        elif self.action in menu_actions:

            actions = menu_actions

        else:

            return None


        for action in actions:

            if action == self.action:
                continue


            bound_key = self.settings.get_control(
                action
            )


            if bound_key == key:

                return action


        return None


    # ====================
    # Navigation
    # ====================

    def go_back(self) -> None:
        """
        Returns to the settings menu.
        """

        self.screen_manager.set_screen(
            self.return_screen
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
        """
        Draws the rebinding screen.
        """

        screen = renderer.screen

        width, height = screen.get_size()


        # ====================
        # Scaling
        # ====================

        scale = min(
            width / 1280,
            height / 720
        )


        title_size = max(
            24,
            int(42 * scale)
        )

        text_size = max(
            16,
            int(26 * scale)
        )

        error_size = max(
            14,
            int(20 * scale)
        )


        title_font = pygame.font.Font(
            None,
            title_size
        )

        text_font = pygame.font.Font(
            None,
            text_size
        )

        error_font = pygame.font.Font(
            None,
            error_size
        )


        # ====================
        # Colours
        # ====================

        white = (
            255,
            255,
            255
        )

        selected_colour = (
            80,
            200,
            255
        )

        error_colour = (
            255,
            100,
            100
        )


        # ====================
        # Positions
        # ====================

        centre_x = width // 2

        title_y = int(
            height * 0.18
        )

        action_y = int(
            height * 0.35
        )

        prompt_y = int(
            height * 0.48
        )

        error_y = int(
            height * 0.62
        )


        # ====================
        # Title
        # ====================

        title = title_font.render(
            "REASSIGN KEY",
            True,
            white
        )

        title_rect = title.get_rect(
            center=(
                centre_x,
                title_y
            )
        )

        screen.blit(
            title,
            title_rect
        )


        # ====================
        # Action Name
        # ====================

        action = text_font.render(
            self.name,
            True,
            selected_colour
        )

        action_rect = action.get_rect(
            center=(
                centre_x,
                action_y
            )
        )

        screen.blit(
            action,
            action_rect
        )


        # ====================
        # Prompt
        # ====================

        prompt = text_font.render(
            "PRESS ANY KEY",
            True,
            white
        )

        prompt_rect = prompt.get_rect(
            center=(
                centre_x,
                prompt_y
            )
        )

        screen.blit(
            prompt,
            prompt_rect
        )


        # ====================
        # Error
        # ====================

        if self.error_message:

            error = error_font.render(
                self.error_message,
                True,
                error_colour
            )

            error_rect = error.get_rect(
                center=(
                    centre_x,
                    error_y
                )
            )

            screen.blit(
                error,
                error_rect
            )
