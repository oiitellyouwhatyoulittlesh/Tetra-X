"""
Tetra-X

File:
    reset_settings.py

Purpose:
    Confirms and performs a full settings reset.
"""

import pygame

from screens.screen import Screen


class ResetSettings(Screen):
    """
    Confirmation screen for resetting all settings.
    """

    def __init__(
        self,
        screen_manager,
        settings,
        return_screen
    ) -> None:

        super().__init__(
            settings
        )

        self.screen_manager = screen_manager
        self.return_screen = return_screen

        self.options = [
            "CANCEL",
            "RESET ALL SETTINGS"
        ]

        self.selected = 0

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

                    self.cancel()


                # ====================
                # Menu Confirm
                # ====================

                elif event.key == self.settings.controls.menu_confirm:

                    self.select()


            elif event.type == pygame.KEYUP:

                if (
                    event.key
                    == self.settings.controls.menu_up
                    and self.navigation_direction == -1
                ):

                    self.navigation_direction = 0


                elif (
                    event.key
                    == self.settings.controls.menu_down
                    and self.navigation_direction == 1
                ):

                    self.navigation_direction = 0


    # ====================
    # Selection
    # ====================

    def select(self) -> None:
        """
        Handles the selected option.
        """

        if self.selected == 0:

            self.cancel()

            return


        if self.selected == 1:

            self.settings.reset()

            self.screen_manager.set_screen(
                self.return_screen
            )


    # ====================
    # Navigation
    # ====================

    def cancel(self) -> None:
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
        """
        Draws the reset confirmation screen.
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
            14,
            int(20 * scale)
        )

        description_size = max(
            12,
            int(17 * scale)
        )


        title_font = pygame.font.Font(
            None,
            title_size
        )

        text_font = pygame.font.Font(
            None,
            text_size
        )

        description_font = pygame.font.Font(
            None,
            description_size
        )


        # ====================
        # Colours
        # ====================

        normal_colour = (
            255,
            255,
            255
        )

        selected_colour = (
            80,
            200,
            255
        )

        muted_colour = (
            150,
            150,
            150
        )


        # ====================
        # Title
        # ====================

        title = title_font.render(
            "RESET ALL SETTINGS?",
            True,
            normal_colour
        )

        title_rect = title.get_rect(
            center=(
                width // 2,
                int(height * 0.20)
            )
        )

        screen.blit(
            title,
            title_rect
        )


        # ====================
        # Description
        # ====================

        lines = [
            "This will restore all controls,",
            "handling settings and other settings",
            "to their default values."
        ]


        y = int(
            height * 0.34
        )


        for line in lines:

            text = description_font.render(
                line,
                True,
                muted_colour
            )

            rect = text.get_rect(
                center=(
                    width // 2,
                    y
                )
            )

            screen.blit(
                text,
                rect
            )

            y += int(
                28 * scale
            )


        # ====================
        # Options
        # ====================

        option_start_y = int(
            height * 0.58
        )

        spacing = int(
            55 * scale
        )


        for index, option in enumerate(
            self.options
        ):

            is_selected = (
                index == self.selected
            )


            colour = (
                selected_colour
                if is_selected
                else normal_colour
            )


            text = text_font.render(
                option,
                True,
                colour
            )


            rect = text.get_rect(
                center=(
                    width // 2,
                    option_start_y
                    + index * spacing
                )
            )


            screen.blit(
                text,
                rect
            )


            if is_selected:

                marker = text_font.render(
                    ">",
                    True,
                    selected_colour
                )

                marker_rect = marker.get_rect(
                    midright=(
                        rect.left
                        - int(18 * scale),
                        rect.centery
                    )
                )

                screen.blit(
                    marker,
                    marker_rect
                )
