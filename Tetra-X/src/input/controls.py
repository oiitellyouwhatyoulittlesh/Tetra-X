"""
Tetra-X

File:
    controls.py

Purpose:
    Handles player input bindings.

"""

import pygame

from settings import Settings


class Controls:
    """
    Handles keyboard controls.
    """

    def __init__(
        self,
        settings: Settings
    ) -> None:

        self.settings = settings


    # ====================
    # Binding
    # ====================

    def get_binding(
        self,
        action: str
    ) -> int | None:
        """
        Returns the key bound to an action.
        """

        return getattr(
            self.settings.controls,
            action,
            None
        )


    # ====================
    # Input Checks
    # ====================

    def pressed(
        self,
        key: int
    ) -> bool:
        """
        Returns True if a key is currently held.
        """

        keys = pygame.key.get_pressed()

        return keys[key]


    def action_pressed(
        self,
        action: str
    ) -> bool:
        """
        Returns True if an action key is held.
        """

        key = self.get_binding(
            action
        )

        if key is None:
            return False

        return self.pressed(
            key
        )


    # ====================
    # Key Events
    # ====================

    def get_event_actions(
        self,
        events
    ) -> list[str]:
        """
        Returns actions triggered this frame.
        """

        actions = []


        for event in events:

            if event.type != pygame.KEYDOWN:
                continue


            for action in (
                "move_left",
                "move_right",
                "soft_drop",
                "hard_drop",
                "rotate_cw",
                "rotate_ccw",
                "rotate_180",
                "hold",
                "pause",
                "restart",
                "menu_up",
                "menu_down",
                "menu_confirm",
                "menu_back"
            ):

                key = self.get_binding(
                    action
                )

                if event.key == key:

                    actions.append(
                        action
                    )


        return actions
