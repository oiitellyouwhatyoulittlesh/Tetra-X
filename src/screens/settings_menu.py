"""
Tetra-X

File:
    settings_menu.py

Purpose:
    Displays and handles the settings menu.
"""

import pygame

from screens.screen import Screen


class SettingsMenu(Screen):
    """
    Main settings menu.

    Allows the player to navigate through:
        - Movement / rotation controls
        - Handling settings
        - Gameplay settings
        - Menu navigation controls
        - Other settings
        - Resetting options
        - Returning to menu
    """

    def __init__(self, screen_manager, settings, previous_screen=None) -> None:
        super().__init__(settings)

        self.screen_manager = screen_manager
        self.previous_screen = previous_screen

        # Menu Entries Configuration
        self.entries = [
            # Movement / Rotation
            {"type": "control", "action": "move_left", "name": "Move Left", "tooltip": "Shift the active piece to the left."},
            {"type": "control", "action": "move_right", "name": "Move Right", "tooltip": "Shift the active piece to the right."},
            {"type": "control", "action": "soft_drop", "name": "Soft Drop", "tooltip": "Accelerate the falling speed of the active piece."},
            {"type": "control", "action": "hard_drop", "name": "Hard Drop", "tooltip": "Instantly drop and lock the active piece to the board."},
            {"type": "control", "action": "rotate_cw", "name": "Clockwise Rotation", "tooltip": "Rotate the piece 90 degrees clockwise."},
            {"type": "control", "action": "rotate_ccw", "name": "Counter Clockwise Rotation", "tooltip": "Rotate the piece 90 degrees counter-clockwise."},
            {"type": "control", "action": "rotate_180", "name": "180 Rotation", "tooltip": "Flip the active piece 180 degrees."},
            {"type": "control", "action": "hold", "name": "Hold", "tooltip": "Store the current piece for later or swap with the held piece."},
            {"type": "control", "action": "pause", "name": "Pause", "tooltip": "Pause or resume the active game."},
            {"type": "control", "action": "restart", "name": "Restart", "tooltip": "Instantly restart the current game session."},

            # Handling
            {"type": "handling", "action": "arr", "name": "Automatic Repeat Rate", "tooltip": "Automatic Repeat Rate: the speed at which pieces move when holding down movement keys, measured in frames per movement."},
            {"type": "handling", "action": "das", "name": "Delayed Auto Shift", "tooltip": "Delayed Auto Shift: the time between the initial keypress and the start of its automatic repeat movement, measured in frames."},
            {"type": "handling", "action": "dcd", "name": "DAS Cut Delay", "tooltip": "DAS Cut Delay: if not 0, any ongoing DAS movement will pause for a set amount of time after dropping/rotating a piece, measured in frames."},
            {"type": "handling", "action": "sdf", "name": "Soft Drop Factor", "tooltip": "Soft Drop Factor: the factor with which soft drops change the gravity speed."},

            # Gameplay
            {"type": "toggle", "action": "prevent_hard_drop", "name": "Prevent Accidental Hard Drops", "tooltip": "If enabled, when a piece locks on its own, the hard drop key becomes unavailable for a few frames. This prevents accidental hard drops."},
            {"type": "toggle", "action": "cancel_das", "name": "Cancel DAS When Changing Directions", "tooltip": "If enabled, DAS charge is cancelled when you change directions."},
            {"type": "toggle", "action": "prefer_soft_drop", "name": "Prefer Soft Drop Over Movement", "tooltip": "If enabled, at very high speeds soft drop will always take precedence over horizontal movement, for a more consistent game feel."},

            # Menu Navigation
            {"type": "control", "action": "menu_up", "name": "Menu Up", "tooltip": "Move selection upward in menus."},
            {"type": "control", "action": "menu_down", "name": "Menu Down", "tooltip": "Move selection downward in menus."},
            {"type": "control", "action": "menu_confirm", "name": "Menu Confirm", "tooltip": "Select or confirm the currently highlighted option."},
            {"type": "control", "action": "menu_back", "name": "Menu Back", "tooltip": "Cancel or return to the previous menu screen."},

            # Other
            {"type": "other_toggle", "action": "display_controls", "name": "Display Controls Ingame", "tooltip": "Toggle on-screen keybind helpers during gameplay."},

            # Reset
            {"type": "reset", "action": "reset", "name": "Reset All Settings", "tooltip": "Restore all controls, handling, and gameplay settings to default."},
            {"type": "reset_data", "action": "reset_data", "name": "Reset All Data", "tooltip": "Erase all high scores, stats, and saved progress."},

            # Back
            {"type": "back", "action": "back", "name": "Back to Menu", "tooltip": "Save changes and return to the main menu."}
        ]

        self.selected = 0
        self.entry_rects: dict[int, pygame.Rect] = {}

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
        Handles mouse movement, scroll, and keyboard events for settings navigation.
        """
        for event in events:
            # Mouse Hover & Click
            if event.type == pygame.MOUSEMOTION:
                for index, rect in self.entry_rects.items():
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in self.entry_rects.items():
                    if rect.collidepoint(event.pos):
                        self.selected = index
                        self.select()
                        return

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.selected = (self.selected - 1) % len(self.entries)
                elif event.y < 0:
                    self.selected = (self.selected + 1) % len(self.entries)

            # Keyboard Navigation
            elif event.type == pygame.KEYDOWN:
                # Menu Up
                if event.key == self.settings.controls.menu_up:
                    self.selected = (self.selected - 1) % len(self.entries)
                    self.navigation_direction = -1
                    self.navigation_timer = -self.navigation_initial_delay

                # Menu Down
                elif event.key == self.settings.controls.menu_down:
                    self.selected = (self.selected + 1) % len(self.entries)
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
        Processes selection of the currently highlighted settings option.
        """
        entry = self.entries[self.selected]

        # Control Rebind
        if entry["type"] == "control":
            from screens.key_bind import Rebind

            self.screen_manager.set_screen(
                Rebind(
                    self.screen_manager,
                    self.settings,
                    entry["action"],
                    entry["name"],
                    self
                )
            )
            return

        # Handling Value Adjustment
        if entry["type"] == "handling":
            from screens.value_select import ValueSelect

            self.screen_manager.set_screen(
                ValueSelect(
                    self.screen_manager,
                    self.settings,
                    entry["action"],
                    entry["name"],
                    self
                )
            )
            return

        # Gameplay Option Toggle
        if entry["type"] == "toggle":
            current = getattr(self.settings.handling, entry["action"])
            setattr(self.settings.handling, entry["action"], not current)
            self.settings.save()
            return

        # Other Settings Toggle
        if entry["type"] == "other_toggle":
            current = getattr(self.settings, entry["action"])
            setattr(self.settings, entry["action"], not current)
            self.settings.save()
            return

        # Reset Settings Confirmation
        if entry["type"] == "reset":
            from screens.reset_settings import ResetSettings

            self.screen_manager.set_screen(
                ResetSettings(self.screen_manager, self.settings, self)
            )
            return

        # Reset Data Confirmation
        if entry["type"] == "reset_data":
            from screens.reset_data import ResetData

            self.screen_manager.set_screen(
                ResetData(self.screen_manager, self.settings, self)
            )
            return

        # Back to Menu
        if entry["type"] == "back":
            self.go_back()
            return


    # ====================
    # Navigation
    # ====================

    def go_back(self) -> None:
        """
        Returns to the previous screen or defaults to the main menu.
        """
        if self.previous_screen:
            self.screen_manager.set_screen(self.previous_screen)
        else:
            from screens.main_menu import MainMenu

            self.screen_manager.set_screen(
                MainMenu(self.screen_manager, self.settings)
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
            ) % len(self.entries)


    # ====================
    # Value Formatters
    # ====================

    def get_value(self, entry) -> str:
        """
        Returns the formatted value string displayed on the right side of an entry.
        """
        entry_type = entry["type"]
        action = entry["action"]

        # Controls
        if entry_type == "control":
            return self.settings.get_control_name(action)

        # Handling
        if entry_type == "handling":
            value = getattr(self.settings.handling, action)

            if action == "sdf":
                if value == float("inf"):
                    return "INF X"
                return f"{value:g} X"

            milliseconds = value * 1000 / 60
            frames = f"{value:.0f}" if value.is_integer() else f"{value:.1f}"

            return f"{milliseconds:.0f} MS  {frames} F"

        # Toggles
        if entry_type in ("toggle", "other_toggle"):
            target = self.settings.handling if entry_type == "toggle" else self.settings
            value = getattr(target, action)
            return "ON" if value else "OFF"

        return ""


    # ====================
    # Rendering
    # ====================

    def draw(self, renderer) -> None:
        """
        Draws the settings menu using a responsive 2 column layout along with the active tooltip.
        """
        screen = renderer.screen
        width, height = screen.get_size()

        # Resolution Scaling Factors
        scale = min(width / 1280, height / 720)

        title_size = max(24, int(42 * scale))
        header_size = max(12, int(17 * scale))
        text_size = max(13, int(20 * scale))

        title_font = pygame.font.Font(None, title_size)
        header_font = pygame.font.Font(None, header_size)
        text_font = pygame.font.Font(None, text_size)

        # UI Colours
        normal_colour = (255, 255, 255)
        selected_colour = (80, 200, 255)
        header_colour = (150, 150, 150)

        # Relative Positions
        left_margin = int(width * 0.08)
        value_x = int(width * 0.72)
        title_y = int(height * 0.035)
        start_y = int(height * 0.105)

        # Build Layout Mapping
        layout = []
        section_names = [
            "MOVEMENT / ROTATION",
            "HANDLING",
            "GAMEPLAY",
            "MENU NAVIGATION",
            "OTHER",
            "RESET & EXIT"
        ]

        for index, entry in enumerate(self.entries):
            if index == 0:
                layout.append(("header", section_names[0], None))
            elif index == 10:
                layout.append(("header", section_names[1], None))
            elif index == 14:
                layout.append(("header", section_names[2], None))
            elif index == 17:
                layout.append(("header", section_names[3], None))
            elif index == 21:
                layout.append(("header", section_names[4], None))
            elif index == 22:
                layout.append(("header", section_names[5], None))

            layout.append(("entry", entry, index))

        # Dynamic Row Spacing Calculation
        row_count = len(layout)
        available_height = height - start_y - int(height * 0.08)
        line_height = max(22, int(available_height / row_count))

        # Draw Title
        title = title_font.render("SETTINGS", True, normal_colour)
        screen.blit(title, (left_margin, title_y))

        # Draw Menu Layout
        y = start_y
        self.entry_rects.clear()

        for item_type, data, index in layout:
            # Section Header
            if item_type == "header":
                header = header_font.render(data, True, header_colour)
                screen.blit(header, (left_margin, y))
                y += line_height
                continue

            entry = data
            is_selected = (index == self.selected)
            colour = selected_colour if is_selected else normal_colour

            # Selected Pointer Marker
            if is_selected:
                marker = text_font.render(">", True, selected_colour)
                screen.blit(marker, (left_margin - int(25 * scale), y))

            # Setting Name
            name = text_font.render(entry["name"], True, colour)
            screen.blit(name, (left_margin, y))

            # Current Value Text
            value_text = self.get_value(entry)

            if value_text:
                value = text_font.render(value_text, True, colour)
                screen.blit(value, (value_x, y))

            # Hover/Click Area Bounds Calculation
            row_width = int(width * 0.84)
            row_rect = pygame.Rect(
                left_margin - int(25 * scale),
                y,
                row_width,
                line_height
            )

            if index is not None:
                self.entry_rects[index] = row_rect

            y += line_height

        # Draw Tooltip at Bottom Center
        selected_entry = self.entries[self.selected]
        tooltip_text = selected_entry.get("tooltip", "")

        if tooltip_text:
            tooltip_size = max(13, int(18 * scale))
            tooltip_font = pygame.font.Font(None, tooltip_size)
            tooltip_surface = tooltip_font.render(tooltip_text, True, (180, 180, 180))
            tooltip_rect = tooltip_surface.get_rect(center=(width // 2, int(height * 0.96)))
            screen.blit(tooltip_surface, tooltip_rect)
