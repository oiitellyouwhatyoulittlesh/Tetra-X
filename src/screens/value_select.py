"""
Tetra-X

File:
    value_select.py

Purpose:
    Allows the player to select a handling setting value
    using keyboard or mouse navigation.
"""

import pygame

from screens.screen import Screen


class ValueSelect(Screen):
    """
    Value selector for handling settings with keyboard and mouse support.
    """

    def __init__(
        self,
        screen_manager,
        settings,
        action: str,
        name: str,
        parent_screen
    ) -> None:
        super().__init__(settings)

        self.screen_manager = screen_manager
        self.action = action
        self.name = name
        self.parent_screen = parent_screen

        self.values = self._build_values()

        current_value = getattr(self.settings.handling, self.action)

        if self.action == "sdf" and current_value == float("inf"):
            self.selected = len(self.values) - 1
        else:
            self.selected = self._find_closest_value(current_value)

        self.visible_rects: dict[int, pygame.Rect] = {}

        # Navigation State
        self.navigation_timer = 0.0
        self.navigation_direction = 0

        self.navigation_initial_delay = 0.30
        self.navigation_repeat_delay = 0.08

        # Mouse Hover State
        self.mouse_hover_cooldown = 0.0
        self.mouse_hover_delay = 0.06


    # ====================
    # Value Construction
    # ====================

    def _build_values(self) -> list[float]:
        """
        Builds the available selectable values array for the target setting action.
        """
        values: list[float] = []

        # Automatic Repeat Rate (ARR)
        if self.action == "arr":
            for i in range(51):
                values.append(i / 10.0)

        # Delayed Auto Shift (DAS)
        elif self.action == "das":
            for i in range(191):
                values.append(1.0 + (i / 10.0))

        # DAS Cut Delay (DCD)
        elif self.action == "dcd":
            for i in range(201):
                values.append(i / 10.0)

        # Soft Drop Factor (SDF)
        elif self.action == "sdf":
            for i in range(5, 41):
                values.append(float(i))
            values.append(float("inf"))

        return values


    def _find_closest_value(self, value: float) -> int:
        """
        Finds the closest selectable value index for the given target float value.
        """
        closest_index = 0
        closest_difference = float("inf")

        for index, selectable in enumerate(self.values):
            if selectable == float("inf"):
                continue

            difference = abs(selectable - value)

            if difference < closest_difference:
                closest_difference = difference
                closest_index = index

        return closest_index


    # ====================
    # Input Handling
    # ====================

    def handle_events(self, events) -> None:
        """
        Handles mouse hover/click, mouse wheel scroll, and keyboard input.
        """
        for event in events:
            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in self.visible_rects.items():
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        self.apply_value()
                        return

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.selected = (self.selected - 1) % len(self.values)
                elif event.y < 0:
                    self.selected = (self.selected + 1) % len(self.values)

            # Keyboard Navigation
            elif event.type == pygame.KEYDOWN:
                # Menu Up
                if event.key == self.settings.controls.menu_up:
                    self.selected = (self.selected - 1) % len(self.values)
                    self.navigation_direction = -1
                    self.navigation_timer = -self.navigation_initial_delay

                # Menu Down
                elif event.key == self.settings.controls.menu_down:
                    self.selected = (self.selected + 1) % len(self.values)
                    self.navigation_direction = 1
                    self.navigation_timer = -self.navigation_initial_delay

                # Menu Confirm
                elif event.key == self.settings.controls.menu_confirm:
                    self.apply_value()

                # Menu Back
                elif event.key == self.settings.controls.menu_back:
                    self.go_back()

            elif event.type == pygame.KEYUP:
                # Stop Held Navigation
                stop_conditions = {
                    self.settings.controls.menu_up: -1,
                    self.settings.controls.menu_down: 1,
                }

                if stop_conditions.get(event.key) == self.navigation_direction:
                    self.navigation_direction = 0


    # ====================
    # Core Update
    # ====================

    def update(self, delta_time: float) -> None:
        """
        Handles key repeat timing and continuous mouse hover navigation.
        """
        # Mouse Hover Cooldown & Continuous Hover Check
        if self.mouse_hover_cooldown > 0:
            self.mouse_hover_cooldown -= delta_time

        if self.mouse_hover_cooldown <= 0:
            mouse_pos = pygame.mouse.get_pos()
            for index, rect in self.visible_rects.items():
                if rect.collidepoint(mouse_pos):
                    if self.selected != index:
                        self.selected = index
                        self.mouse_hover_cooldown = self.mouse_hover_delay
                    break

        # Keyboard Navigation Repeat
        if self.navigation_direction == 0:
            return

        self.navigation_timer += delta_time

        if self.navigation_timer < 0:
            return

        while self.navigation_timer >= self.navigation_repeat_delay:
            self.navigation_timer -= self.navigation_repeat_delay
            self.selected = (
                self.selected + self.navigation_direction
            ) % len(self.values)


    # ====================
    # Selection Handling
    # ====================

    def apply_value(self) -> None:
        """
        Applies the selected handling value to active settings and returns to parent screen.
        """
        value = self.values[self.selected]
        setattr(self.settings.handling, self.action, value)
        self.settings.save()
        self.go_back()


    def go_back(self) -> None:
        """
        Returns to the parent settings screen.
        """
        self.screen_manager.set_screen(self.parent_screen)


    # ====================
    # Rendering
    # ====================

    def draw(self, renderer) -> None:
        """
        Draws the scroll wheel value selector interface.
        """
        screen = renderer.screen
        width, height = screen.get_size()

        # Resolution Scaling Factors
        scale = min(width / 1280, height / 720)

        title_size = max(24, int(42 * scale))
        text_size = max(18, int(28 * scale))
        small_size = max(14, int(20 * scale))

        title_font = pygame.font.Font(None, title_size)
        text_font = pygame.font.Font(None, text_size)
        small_font = pygame.font.Font(None, small_size)

        # UI Colours
        normal_colour = (255, 255, 255)
        selected_colour = (80, 200, 255)

        # Title Rendering
        title = title_font.render(self.name, True, normal_colour)
        title_rect = title.get_rect(center=(width // 2, int(height * 0.16)))
        screen.blit(title, title_rect)

        # Scroll Wheel Items Setup
        visible_count = 7
        center_y = int(height * 0.50)
        spacing = int(48 * scale)
        half = visible_count // 2

        self.visible_rects.clear()

        for offset in range(-half, half + 1):
            index = self.selected + offset

            if index < 0 or index >= len(self.values):
                continue

            value = self.values[index]

            if value == float("inf"):
                text = "INF X"
            elif self.action == "sdf":
                text = f"{value:g} X"
            else:
                milliseconds = value * 1000 / 60
                frames = f"{value:.0f}" if value.is_integer() else f"{value:.1f}"
                text = f"{milliseconds:.0f} MS  {frames} F"

            colour = selected_colour if offset == 0 else normal_colour
            font = text_font if offset == 0 else small_font

            rendered = font.render(text, True, colour)
            rendered_rect = rendered.get_rect(
                center=(width // 2, center_y + offset * spacing)
            )

            screen.blit(rendered, rendered_rect)

            hitbox = rendered_rect.inflate(40, 10)
            self.visible_rects[index] = hitbox
