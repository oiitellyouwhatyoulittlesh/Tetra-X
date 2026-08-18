"""
Tetra-X

File:
    mode_select.py

Purpose:
    Displays and handles game mode selection.
"""

import pygame

from game.modes import GameMode
from screens.game_screen import GameScreen
from screens.screen import Screen


class ModeSelect(Screen):
    """
    Game mode selection screen.
    """

    def __init__(self, screen_manager, settings) -> None:
        super().__init__(settings)

        self.screen_manager = screen_manager

        self.options = [
            "ZEN",
            "BLITZ",
            "40 LINES",
            "BACK"
        ]

        # Tooltips mapped by option name
        self.tooltips = {
            "ZEN": "Relax or train in this neverending mode.",
            "BLITZ": "A two-minute race against the clock.",
            "40 LINES": "Complete 40 lines as quickly as possible.",
            "BACK": "Return to the main menu."
        }

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
        Handles mouse and keyboard inputs for mode menu navigation.
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

                # Menu Back
                elif event.key == self.settings.controls.menu_back:
                    self.go_back()

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
        Handles activation for the currently selected game mode option.
        """
        option = self.options[self.selected]

        if option == "ZEN":
            self.start_game(GameMode.ZEN)
        elif option == "BLITZ":
            self.start_game(GameMode.BLITZ)
        elif option == "40 LINES":
            self.start_game(GameMode.FORTY_LINES)
        elif option == "BACK":
            self.go_back()


    def go_back(self) -> None:
        """
        Returns to the main menu screen.
        """
        from screens.main_menu import MainMenu

        self.screen_manager.set_screen(
            MainMenu(self.screen_manager, self.settings)
        )


    def start_game(self, mode: GameMode) -> None:
        """
        Launches gameplay using the specified game mode.
        """
        self.screen_manager.set_screen(
            GameScreen(self.screen_manager, mode)
        )


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
        Draws the game mode selection screen via the renderer and renders the current tooltip.
        """
        self.option_rects = renderer.draw_menu(
            "SELECT MODE",
            self.options,
            self.selected
        )

        # Draw Tooltip at Bottom Center
        screen = renderer.screen
        width, height = screen.get_size()
        scale = min(width / 1280, height / 720)

        current_option = self.options[self.selected]
        tooltip_text = self.tooltips.get(current_option, "")

        if tooltip_text:
            tooltip_size = max(14, int(20 * scale))
            tooltip_font = pygame.font.Font(None, tooltip_size)
            tooltip_surface = tooltip_font.render(tooltip_text, True, (180, 180, 180))
            tooltip_rect = tooltip_surface.get_rect(center=(width // 2, int(height * 0.92)))
            screen.blit(tooltip_surface, tooltip_rect)
