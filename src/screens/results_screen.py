"""
Tetra-X

File:
    results_screen.py

Purpose:
    Displays the results of a completed Blitz or 40 Lines run.
"""

import pygame

from game.modes import GameMode
from screens.screen import Screen


class ResultsScreen(Screen):
    """
    Displays the results and personal records for a completed game session.
    """

    def __init__(
        self,
        screen_manager,
        settings,
        mode: GameMode,
        results: dict,
        new_record: bool,
        record_difference: float,
        topped_out: bool = False
    ) -> None:
        super().__init__(settings)

        self.screen_manager = screen_manager
        self.mode = mode

        self.results = results
        self.new_record = new_record
        self.record_difference = record_difference
        self.topped_out = topped_out

        self.options = [
            "RETRY",
            "BACK TO MENU"
        ]

        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

        # Navigation State
        self.navigation_timer = 0.0
        self.navigation_direction = 0

        self.navigation_initial_delay = 0.30
        self.navigation_repeat_delay = 0.08

        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.main_font = pygame.font.Font(None, 52)
        self.stat_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)


    # ====================
    # Formatting Utilities
    # ====================

    def format_time(self, seconds: float) -> str:
        """
        Formats seconds as M:SS.mmm.
        """
        minutes = int(seconds // 60)
        remaining = seconds - minutes * 60
        return f"{minutes}:{remaining:06.3f}"


    # ====================
    # Input Handling
    # ====================

    def handle_events(self, events) -> None:
        """
        Handles mouse and keyboard input for results screen navigation.
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
                # Stop Navigation
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
        Executes the highlighted action.
        """
        option = self.options[self.selected]

        if option == "RETRY":
            from screens.game_screen import GameScreen

            self.screen_manager.set_screen(
                GameScreen(self.screen_manager, self.mode)
            )

        elif option == "BACK TO MENU":
            from screens.main_menu import MainMenu

            self.screen_manager.set_screen(
                MainMenu(self.screen_manager, self.settings)
            )


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
    # Drawing Helpers
    # ====================

    def draw_text(
        self,
        renderer,
        text: str,
        font,
        position: tuple[int, int],
        centre: bool = True
    ) -> None:
        """
        Renders a text string at a specified position on screen.
        """
        surface = font.render(text, True, (255, 255, 255))

        if centre:
            rectangle = surface.get_rect(center=position)
        else:
            rectangle = surface.get_rect(midleft=position)

        renderer.screen.blit(surface, rectangle)


    # ====================
    # Rendering
    # ====================

    def draw(self, renderer) -> None:
        """
        Draws score/time results, personal records, statistics, and menu buttons.
        """
        renderer.clear()
        screen = renderer.screen
        centre_x = renderer.screen_width // 2

        # Title Text
        title = "TOP OUT" if self.topped_out else "RESULTS"
        title_surface = self.title_font.render(title, True, (255, 255, 255))
        title_rectangle = title_surface.get_rect(center=(centre_x, 100))
        screen.blit(title_surface, title_rectangle)

        # Primary Result Indicator
        if self.mode == GameMode.BLITZ:
            main_value = str(self.results["score"])
            main_label = "SCORE"
        else:
            main_value = self.format_time(self.results["time"])
            main_label = "TIME"

        label_surface = self.main_font.render(main_label, True, (180, 180, 180))
        label_rectangle = label_surface.get_rect(center=(centre_x, 190))
        screen.blit(label_surface, label_rectangle)

        value_surface = self.title_font.render(main_value, True, (255, 220, 0))
        value_rectangle = value_surface.get_rect(center=(centre_x, 255))
        screen.blit(value_surface, value_rectangle)

        # Personal Best Delta Text
        if self.topped_out:
            pb_text = None
        elif self.new_record:
            pb_text = "NEW PERSONAL BEST!"
        elif self.mode == GameMode.BLITZ:
            difference = self.record_difference
            pb_text = (
                f"+{difference:,} FROM PB"
                if difference >= 0
                else f"{difference:,} FROM PB"
            )
        else:
            difference = self.record_difference
            pb_text = (
                f"{abs(difference):.3f}s FASTER THAN PB"
                if difference < 0
                else f"{difference:.3f}s SLOWER THAN PB"
            )

        if pb_text is not None:
            pb_surface = self.stat_font.render(pb_text, True, (255, 255, 255))
            pb_rectangle = pb_surface.get_rect(center=(centre_x, 320))
            screen.blit(pb_surface, pb_rectangle)

        # Game Statistics Grid
        stats = [
            ("LINES", str(self.results["lines"])),
            ("PIECES", str(self.results["pieces"])),
            ("PPS", f'{self.results["pps"]:.2f}'),
            ("INPUTS", str(self.results["inputs"])),
            ("IPP", f'{self.results["inputs_per_piece"]:.2f}'),
            ("LEVEL", str(self.results["level"]))
        ]

        start_y = 400
        left_x = centre_x - 250
        right_x = centre_x + 50

        for index, (label, value) in enumerate(stats):
            column = index % 2
            row = index // 2

            x = left_x if column == 0 else right_x
            y = start_y + row * 55

            text = f"{label}: {value}"
            surface = self.stat_font.render(text, True, (255, 255, 255))
            rectangle = surface.get_rect(midleft=(x, y))
            screen.blit(surface, rectangle)

        # Menu Options
        normal_colour = (255, 255, 255)
        selected_colour = (80, 200, 255)
        start_y = renderer.screen_height - 150

        self.option_rects = []

        for index, option in enumerate(self.options):
            is_selected = (index == self.selected)
            colour = selected_colour if is_selected else normal_colour
            text = f"> {option}" if is_selected else option

            surface = self.main_font.render(text, True, colour)
            rectangle = surface.get_rect(
                center=(centre_x, start_y + index * 60)
            )

            screen.blit(surface, rectangle)
            self.option_rects.append(rectangle)
