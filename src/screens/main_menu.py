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

    def __init__(self, screen_manager, settings) -> None:
        super().__init__(settings)

        self.screen_manager = screen_manager

        self.options = [
            "PLAY",
            "SETTINGS",
            "QUIT"
        ]

        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

        # Navigation State
        self.navigation_timer = 0.0
        self.navigation_direction = 0

        self.navigation_initial_delay = 0.30
        self.navigation_repeat_delay = 0.08


    # ====================
    # Input Handling
    # ====================

    def handle_events(self, events) -> None:
        """
        Handles mouse and keyboard inputs for menu navigation.
        """
        for event in events:
            # Mouse Input
            if event.type == pygame.MOUSEMOTION:
                for index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        self.select()
                        return

            # Keyboard Input
            elif event.type == pygame.KEYDOWN:
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

                # Menu Confirm
                elif event.key == self.settings.controls.menu_confirm:
                    self.select()

            elif event.type == pygame.KEYUP:
                # Stop Held Navigation
                stop_conditions = {
                    self.settings.controls.menu_up: -1,
                    self.settings.controls.menu_down: 1,
                }

                if stop_conditions.get(event.key) == self.navigation_direction:
                    self.navigation_direction = 0


    # ====================
    # Selection Handling
    # ====================

    def select(self) -> None:
        """
        Triggers actions for the currently selected menu option.
        """
        option = self.options[self.selected]

        if option == "PLAY":
            from screens.mode_select import ModeSelect

            self.screen_manager.set_screen(
                ModeSelect(self.screen_manager, self.settings)
            )

        elif option == "SETTINGS":
            from screens.settings_menu import SettingsMenu

            self.screen_manager.set_screen(
                SettingsMenu(self.screen_manager, self.settings)
            )

        elif option == "QUIT":
            pygame.event.post(pygame.event.Event(pygame.QUIT))


    # ====================
    # Core Update
    # ====================

    def update(self, delta_time: float) -> None:
        """
        Handles key repeat timing for held directional navigation.
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
        Draws the main menu screen via the renderer.
        """
        self.option_rects = renderer.draw_menu(
            "TETRA-X",
            self.options,
            self.selected
        )
