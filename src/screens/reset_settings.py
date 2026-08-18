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
    Confirmation screen for resetting all user settings to default.
    """

    def __init__(self, screen_manager, settings, return_screen) -> None:
        super().__init__(settings)

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

        self.option_rects: list[pygame.Rect] = []


    # ====================
    # Input Handling
    # ====================

    def handle_events(self, events) -> None:
        """
        Handles keyboard and mouse input for resetting settings options.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Menu Up
                if event.key == self.settings.controls.menu_up:
                    self.selected = (self.selected - 1) % len(self.options)
                    self.navigation_direction = -1
                    self.navigation_timer = -self.navigation_initial_delay

                # Menu Down
                elif event.key == self.settings.controls.menu_down:
                    self.selected = (self.selected + 1) % len(self.options)
                    self.navigation_direction = 1
                    self.navigation_timer = -self.navigation_initial_delay

                # Menu Back
                elif event.key == self.settings.controls.menu_back:
                    self.cancel()

                # Menu Confirm
                elif event.key == self.settings.controls.menu_confirm:
                    self.select()

            elif event.type == pygame.KEYUP:
                # Stop Navigation
                stop_conditions = {
                    self.settings.controls.menu_up: -1,
                    self.settings.controls.menu_down: 1,
                }

                if stop_conditions.get(event.key) == self.navigation_direction:
                    self.navigation_direction = 0

            # Mouse Hover
            elif event.type == pygame.MOUSEMOTION:
                for index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        break

            # Mouse Click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        self.select()
                        break


    # ====================
    # Selection Handling
    # ====================

    def select(self) -> None:
        """
        Executes the selected action.
        """
        if self.selected == 0:
            self.cancel()
            return

        if self.selected == 1:
            self.settings.reset()
            self.screen_manager.set_screen(self.return_screen)


    def cancel(self) -> None:
        """
        Returns to the settings menu.
        """
        self.screen_manager.set_screen(self.return_screen)


    # ====================
    # Core Update
    # ====================

    def update(self, delta_time: float) -> None:
        """
        Handles key repeat timing for held menu navigation.
        """
        if self.navigation_direction == 0:
            return

        self.navigation_timer += delta_time

        if self.navigation_timer < 0:
            return

        while self.navigation_timer >= self.navigation_repeat_delay:
            self.navigation_timer -= self.navigation_repeat_delay
            self.selected = (
                self.selected + self.navigation_direction
            ) % len(self.options)


    # ====================
    # Rendering
    # ====================

    def draw(self, renderer) -> None:
        """
        Draws the reset confirmation interface.
        """
        screen = renderer.screen
        width, height = screen.get_size()

        # Resolution Scaling Factors
        scale = min(width / 1280, height / 720)

        title_size = max(24, int(42 * scale))
        text_size = max(14, int(20 * scale))
        description_size = max(12, int(17 * scale))

        title_font = pygame.font.Font(None, title_size)
        text_font = pygame.font.Font(None, text_size)
        description_font = pygame.font.Font(None, description_size)

        # UI Colours
        normal_colour = (255, 255, 255)
        selected_colour = (80, 200, 255)
        muted_colour = (150, 150, 150)

        # Title Text
        title = title_font.render("RESET ALL SETTINGS?", True, normal_colour)
        title_rect = title.get_rect(center=(width // 2, int(height * 0.20)))
        screen.blit(title, title_rect)

        # Description Lines
        lines = [
            "This will restore all controls,",
            "handling settings and other settings",
            "to their default values."
        ]

        y = int(height * 0.34)

        for line in lines:
            text = description_font.render(line, True, muted_colour)
            rect = text.get_rect(center=(width // 2, y))
            screen.blit(text, rect)
            y += int(28 * scale)

        # Options Rendering
        option_start_y = int(height * 0.58)
        spacing = int(55 * scale)

        self.option_rects.clear()

        for index, option in enumerate(self.options):
            is_selected = (index == self.selected)
            colour = selected_colour if is_selected else normal_colour

            text = text_font.render(option, True, colour)
            rect = text.get_rect(
                center=(width // 2, option_start_y + index * spacing)
            )

            self.option_rects.append(rect)
            screen.blit(text, rect)

            if is_selected:
                marker = text_font.render(">", True, selected_colour)
                marker_rect = marker.get_rect(
                    midright=(rect.left - int(18 * scale), rect.centery)
                )
                screen.blit(marker, marker_rect)
