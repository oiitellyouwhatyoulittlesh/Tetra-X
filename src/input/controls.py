"""
Tetra-X

File:
    controls.py

Purpose:
    Handles player input bindings.

"""

import pygame


class Controls:
    """
    Handles keyboard controls.
    """

    def __init__(self) -> None:

        self.bindings = {
            "move_left": pygame.K_LEFT,
            "move_right": pygame.K_RIGHT,
            "soft_drop": pygame.K_DOWN,

            "hard_drop": pygame.K_SPACE,

            "rotate_cw": pygame.K_UP,
            "rotate_ccw": pygame.K_z,
            "rotate_180": pygame.K_x,

            "hold": pygame.K_c,

            "pause": pygame.K_ESCAPE,
            "restart": pygame.K_r
        }


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

        if action not in self.bindings:
            return False

        return self.pressed(
            self.bindings[action]
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


            for action, key in self.bindings.items():

                if event.key == key:

                    actions.append(action)


        return actions


    # ====================
    # Information
    # ====================

    def set_binding(
        self,
        action: str,
        key: int
    ) -> None:
        """
        Changes an action key.
        """

        self.bindings[action] = key


    def get_binding(
        self,
        action: str
    ) -> int | None:
        """
        Returns the key for an action.
        """

        return self.bindings.get(action)
