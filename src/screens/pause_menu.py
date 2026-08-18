"""
Tetra-X

File:
    pause_menu.py

Purpose:
    Displays and handles the pause menu overlay and options.
"""

import pygame

from game.modes import GameMode
from input.controls import Controls
from screens.screen import Screen


class PauseMenu(Screen):
    """
    Pause menu screen.
    """

    def __init__(self, screen_manager, game_screen, settings) -> None:
        super().__init__(settings)

        self.screen_manager = screen_manager
        self.game_screen = game_screen
        self.settings = settings

        self.controls = Controls(settings)

        # Menu Options Configuration
        if self.game_screen.game.mode == GameMode.ZEN:
            self.options = [
                "RESUME",
                "RESTART",
                "QUIT TO MENU"
            ]
        else:
            self.options = [
                "RESTART",
                "QUIT TO MENU"
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
        Handles mouse and action bound keyboard inputs for the pause menu.
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

        actions = self.controls.get_event_actions(events)

        for action in actions:
            # Menu Up
            if action == "menu_up":
                self.selected = (self.selected - 1) % len(self.options)
                self.navigation_direction = -1
                self.navigation_timer = -self.navigation_initial_delay

            # Menu Down
            elif action == "menu_down":
                self.selected = (self.selected + 1) % len(self.options)
                self.navigation_direction = 1
                self.navigation_timer = -self.navigation_initial_delay

            # Menu Back
            elif action == "menu_back":
                if self.game_screen.game.mode == GameMode.ZEN:
                    self.resume()

            # Menu Confirm
            elif action == "menu_confirm":
                self.select()

            # Restart Action Key
            elif action == "restart":
                self.restart()

        # Stop Navigation on Key Release
        for event in events:
            if event.type != pygame.KEYUP:
                continue

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
        Handles execution of the currently highlighted pause menu option.
        """
        option = self.options[self.selected]

        if option == "RESUME":
            self.resume()
        elif option == "RESTART":
            self.restart()
        elif option == "QUIT TO MENU":
            from screens.main_menu import MainMenu

            self.screen_manager.set_screen(
                MainMenu(self.screen_manager, self.settings)
            )


    def resume(self) -> None:
        """
        Unpauses the game and returns to active gameplay screen.
        """
        self.game_screen.game.paused = False
        self.game_screen.events = []
        self.game_screen.game.input.reset_handling()

        self.screen_manager.set_screen(self.game_screen)


    def restart(self) -> None:
        """
        Resets and restarts the current gameplay session.
        """
        self.game_screen.game.restart()
        self.game_screen.events = []

        self.screen_manager.set_screen(self.game_screen)


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
        Draws the pause menu overlay using the renderer.
        """
        self.option_rects = renderer.draw_menu(
            "PAUSED",
            self.options,
            self.selected
        )
