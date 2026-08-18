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
        - Resetting all settings
    """

    def __init__(
        self,
        screen_manager,
        settings,
        previous_screen=None
    ) -> None:

        super().__init__(
            settings
        )

        self.screen_manager = screen_manager
        self.previous_screen = previous_screen

        # ====================
        # Menu Entries
        # ====================

        self.entries = [

            # Movement / Rotation

            {
                "type": "control",
                "action": "move_left",
                "name": "Move Left"
            },

            {
                "type": "control",
                "action": "move_right",
                "name": "Move Right"
            },

            {
                "type": "control",
                "action": "soft_drop",
                "name": "Soft Drop"
            },

            {
                "type": "control",
                "action": "hard_drop",
                "name": "Hard Drop"
            },

            {
                "type": "control",
                "action": "rotate_cw",
                "name": "Clockwise Rotation"
            },

            {
                "type": "control",
                "action": "rotate_ccw",
                "name": "Counter Clockwise Rotation"
            },

            {
                "type": "control",
                "action": "rotate_180",
                "name": "180 Rotation"
            },

            {
                "type": "control",
                "action": "hold",
                "name": "Hold"
            },

            {
                "type": "control",
                "action": "pause",
                "name": "Pause"
            },

            {
                "type": "control",
                "action": "restart",
                "name": "Restart"
            },


            # Handling

            {
                "type": "handling",
                "action": "arr",
                "name": "Automatic Repeat Rate"
            },

            {
                "type": "handling",
                "action": "das",
                "name": "Delayed Auto Shift"
            },

            {
                "type": "handling",
                "action": "dcd",
                "name": "DAS Cut Delay"
            },

            {
                "type": "handling",
                "action": "sdf",
                "name": "Soft Drop Factor"
            },


            # Gameplay

            {
                "type": "toggle",
                "action": "prevent_hard_drop",
                "name": "Prevent Accidental Hard Drops"
            },

            {
                "type": "toggle",
                "action": "cancel_das",
                "name": "Cancel DAS When Changing Directions"
            },

            {
                "type": "toggle",
                "action": "prefer_soft_drop",
                "name": "Prefer Soft Drop Over Movement"
            },


            # Menu Navigation

            {
                "type": "control",
                "action": "menu_up",
                "name": "Menu Up"
            },

            {
                "type": "control",
                "action": "menu_down",
                "name": "Menu Down"
            },

            {
                "type": "control",
                "action": "menu_confirm",
                "name": "Menu Confirm"
            },

            {
                "type": "control",
                "action": "menu_back",
                "name": "Menu Back"
            },


            # Reset

            {
                "type": "reset",
                "action": "reset",
                "name": "Reset All Settings"
            },

            {
                "type": "reset_data",
                "action": "reset_data",
                "name": "Reset All Data"
            }
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
                    ) % len(self.entries)

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
                    ) % len(self.entries)

                    self.navigation_direction = 1
                    self.navigation_timer = (
                        -self.navigation_initial_delay
                    )


                # ====================
                # Menu Back
                # ====================

                elif event.key == self.settings.controls.menu_back:

                    self.go_back()


                # ====================
                # Menu Confirm
                # ====================

                elif event.key == self.settings.controls.menu_confirm:

                    self.select()


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
    # Selection
    # ====================

    def select(self) -> None:
        """
        Handles the selected setting.
        """

        entry = self.entries[
            self.selected
        ]


        # ====================
        # Control Rebind
        # ====================

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


        # ====================
        # Handling Value
        # ====================

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


        # ====================
        # Toggle
        # ====================

        if entry["type"] == "toggle":

            current = getattr(
                self.settings.handling,
                entry["action"]
            )

            setattr(
                self.settings.handling,
                entry["action"],
                not current
            )

            self.settings.save()

            return


        # ====================
        # Reset
        # ====================

        if entry["type"] == "reset":

            from screens.reset_settings import ResetSettings

            self.screen_manager.set_screen(
                ResetSettings(
                    self.screen_manager,
                    self.settings,
                    self
                )
            )

            return
        
        if entry["type"] == "reset_data":

            from screens.reset_data import ResetData

            self.screen_manager.set_screen(
                ResetData(
                    self.screen_manager,
                    self.settings,
                    self
                )
            )

            return


    # ====================
    # Navigation
    # ====================

    def go_back(self) -> None:
        """
        Returns to the previous screen or the main menu.
        """

        if self.previous_screen:

            self.screen_manager.set_screen(
                self.previous_screen
            )

        else:

            from screens.main_menu import MainMenu

            self.screen_manager.set_screen(
                MainMenu(
                    self.screen_manager,
                    self.settings
                )
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
        

        while(
            self.navigation_timer
            >= self.navigation_repeat_delay
        ):

            self.navigation_timer -= (
                self.navigation_repeat_delay
            )


            self.selected = (
                self.selected
                + self.navigation_direction
            ) % len(self.entries)


    # ====================
    # Values
    # ====================

    def get_value(
        self,
        entry
    ) -> str:
        """
        Returns the value displayed on the right
        side of the settings entry.
        """

        entry_type = entry["type"]
        action = entry["action"]


        # ====================
        # Controls
        # ====================

        if entry_type == "control":

            return self.settings.get_control_name(
                action
            )


        # ====================
        # Handling
        # ====================

        if entry_type == "handling":

            value = getattr(
                self.settings.handling,
                action
            )


            if action == "sdf":

                if value == float("inf"):

                    return "INF X"

                return f"{value:g} X"


            milliseconds = (
                value * 1000 / 60
            )

            if value.is_integer():

                frames = f"{value:.0f}"
            
            else:

                frames = f"{value:.1f}"

            return (
                f"{milliseconds:.0f} MS  "
                f"{frames} F"
            )


        # ====================
        # Toggles
        # ====================

        if entry_type == "toggle":

            value = getattr(
                self.settings.handling,
                action
            )

            return (
                "ON"
                if value
                else "OFF"
            )


        # ====================
        # Reset
        # ====================

        if entry_type == "reset":

            return ""


        return ""


    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        renderer
    ) -> None:
        """
        Draws the settings menu using a responsive
        two-column layout.
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

        header_size = max(
            12,
            int(17 * scale)
        )

        text_size = max(
            13,
            int(20 * scale)
        )


        title_font = pygame.font.Font(
            None,
            title_size
        )

        header_font = pygame.font.Font(
            None,
            header_size
        )

        text_font = pygame.font.Font(
            None,
            text_size
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

        header_colour = (
            150,
            150,
            150
        )


        # ====================
        # Positions
        # ====================

        left_margin = int(
            width * 0.08
        )

        value_x = int(
            width * 0.72
        )

        title_y = int(
            height * 0.035
        )

        start_y = int(
            height * 0.105
        )


        # ====================
        # Build Layout
        # ====================

        layout = []

        section_names = [
            "MOVEMENT / ROTATION",
            "HANDLING",
            "GAMEPLAY",
            "MENU NAVIGATION",
            "OTHER"
        ]

        for index, entry in enumerate(
            self.entries
        ):

            if index == 0:

                layout.append(
                    (
                        "header",
                        section_names[0],
                        None
                    )
                )

            elif index == 10:

                layout.append(
                    (
                        "header",
                        section_names[1],
                        None
                    )
                )

            elif index == 14:

                layout.append(
                    (
                        "header",
                        section_names[2],
                        None
                    )
                )

            elif index == 17:

                layout.append(
                    (
                        "header",
                        section_names[3],
                        None
                    )
                )

            elif index == 21:

                layout.append(
                    (
                        "header",
                        section_names[4],
                        None
                    )
                )


            layout.append(
                (
                    "entry",
                    entry,
                    index
                )
            )


        # ====================
        # Calculate Spacing
        # ====================

        row_count = len(
            layout
        )

        available_height = (
            height
            - start_y
            - int(height * 0.05)
        )

        line_height = max(
            22,
            int(
                available_height
                / row_count
            )
        )


        # ====================
        # Title
        # ====================

        title = title_font.render(
            "SETTINGS",
            True,
            normal_colour
        )

        screen.blit(
            title,
            (
                left_margin,
                title_y
            )
        )


        # ====================
        # Draw Layout
        # ====================

        y = start_y


        for item_type, data, index in layout:

            # ====================
            # Section Header
            # ====================

            if item_type == "header":

                header = header_font.render(
                    data,
                    True,
                    header_colour
                )

                screen.blit(
                    header,
                    (
                        left_margin,
                        y
                    )
                )

                y += line_height

                continue


            entry = data

            is_selected = (
                index == self.selected
            )


            # ====================
            # Colours
            # ====================

            colour = (
                selected_colour
                if is_selected
                else normal_colour
            )


            # ====================
            # Selected Marker
            # ====================

            if is_selected:

                marker = text_font.render(
                    ">",
                    True,
                    selected_colour
                )

                screen.blit(
                    marker,
                    (
                        left_margin
                        - int(25 * scale),
                        y
                    )
                )


            # ====================
            # Setting Name
            # ====================

            name = text_font.render(
                entry["name"],
                True,
                colour
            )

            screen.blit(
                name,
                (
                    left_margin,
                    y
                )
            )


            # ====================
            # Current Value
            # ====================

            value_text = self.get_value(
                entry
            )


            if value_text:

                value = text_font.render(
                    value_text,
                    True,
                    colour
                )

                screen.blit(
                    value,
                    (
                        value_x,
                        y
                    )
                )


            y += line_height
