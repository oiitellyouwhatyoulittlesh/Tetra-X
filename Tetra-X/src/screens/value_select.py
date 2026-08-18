"""
Tetra-X

File:
    value_select.py

Purpose:
    Allows the player to select a handling setting value
    using keyboard navigation.
"""

import pygame

from screens.screen import Screen


class ValueSelect(Screen):
    """
    Keyboard-based value selector for handling settings.
    """

    def __init__(
        self,
        screen_manager,
        settings,
        action: str,
        name: str,
        parent_screen
    ) -> None:

        super().__init__(
            settings
        )

        self.screen_manager = screen_manager
        self.action = action
        self.name = name
        self.parent_screen = parent_screen

        self.values = self._build_values()

        current_value = getattr(
            self.settings.handling,
            self.action
        )

        if self.action == "sdf" and current_value == float("inf"):

            self.selected = len(
                self.values
            ) - 1

        else:

            self.selected = self._find_closest_value(
                current_value
            )


        self.navigation_timer = 0.0
        self.navigation_direction = 0

        self.navigation_initial_delay = 0.30
        self.navigation_repeat_delay = 0.08


    # ====================
    # Values
    # ====================

    def _build_values(self) -> list[float]:
        """
        Builds the available values for the selected setting.
        """

        values: list[float] = []


        # ====================
        # ARR
        # ====================

        if self.action == "arr":

            # 0.0 -> 5.0 in 0.1 increments

            for i in range(51):

                values.append(
                    i / 10.0
                )


        # ====================
        # DAS
        # ====================

        elif self.action == "das":

            # 1.0 -> 20.0 in 0.1 increments

            for i in range(191):

                values.append(
                    1.0 + (i / 10.0)
                )


        # ====================
        # DCD
        # ====================

        elif self.action == "dcd":

            # 0.0 -> 20.0 in 0.1 increments

            for i in range(201):

                values.append(
                    i / 10.0
                )


        # ====================
        # SDF
        # ====================

        elif self.action == "sdf":

            # 5.0 -> 40.0 in 1.0 increments

            for i in range(5, 41):

                values.append(
                    float(i)
                )

            # Infinite SDF

            values.append(
                float("inf")
            )


        return values


    def _find_closest_value(
        self,
        value: float
    ) -> int:
        """
        Finds the closest selectable value.
        """

        closest_index = 0
        closest_difference = float("inf")

        for index, selectable in enumerate(
            self.values
        ):

            if selectable == float("inf"):

                continue

            difference = abs(
                selectable - value
            )

            if difference < closest_difference:

                closest_difference = difference
                closest_index = index


        return closest_index


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
                    ) % len(self.values)

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
                    ) % len(self.values)

                    self.navigation_direction = 1

                    self.navigation_timer = (
                        -self.navigation_initial_delay
                    )


                # ====================
                # Menu Confirm
                # ====================

                elif event.key == self.settings.controls.menu_confirm:

                    self.apply_value()


                # ====================
                # Menu Back
                # ====================

                elif event.key == self.settings.controls.menu_back:

                    self.go_back()


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
            ) % len(self.values)


    # ====================
    # Selection
    # ====================

    def apply_value(self) -> None:
        """
        Applies the selected value to the settings.
        """

        value = self.values[
            self.selected
        ]

        setattr(
            self.settings.handling,
            self.action,
            value
        )

        self.settings.save()

        self.go_back()


    # ====================
    # Navigation
    # ====================

    def go_back(self) -> None:
        """
        Returns to the settings menu.
        """

        self.screen_manager.set_screen(
            self.parent_screen
        )


    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        renderer
    ) -> None:
        """
        Draws the scroll-wheel value selector.
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
            18,
            int(28 * scale)
        )

        small_size = max(
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

        small_font = pygame.font.Font(
            None,
            small_size
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


        # ====================
        # Title
        # ====================

        title = title_font.render(
            self.name,
            True,
            normal_colour
        )

        title_rect = title.get_rect(
            center=(
                width // 2,
                int(height * 0.16)
            )
        )

        screen.blit(
            title,
            title_rect
        )


        # ====================
        # Scroll Wheel
        # ====================

        visible_count = 7

        center_y = int(
            height * 0.50
        )

        spacing = int(
            48 * scale
        )


        half = visible_count // 2


        for offset in range(
            -half,
            half + 1
        ):

            index = (
                self.selected
                + offset
            )

            if index < 0 or index >= len(self.values):

                continue


            value = self.values[
                index
            ]


            if value == float("inf"):

                text = "INF X"

            elif self.action == "sdf":

                text = f"{value:g} X"

            else:

                milliseconds = (
                    value * 1000 / 60
                )

                if value.is_integer():

                    frames = f"{value:.0f}"

                else:

                    frames = f"{value:.1f}"

                text = (
                    f"{milliseconds:.0f} MS  "
                    f"{frames} F"
                )


            colour = (
                selected_colour
                if offset == 0
                else normal_colour
            )


            font = (
                text_font
                if offset == 0
                else small_font
            )


            rendered = font.render(
                text,
                True,
                colour
            )

            rendered_rect = rendered.get_rect(
                center=(
                    width // 2,
                    center_y
                    + offset * spacing
                )
            )

            screen.blit(
                rendered,
                rendered_rect
            )
