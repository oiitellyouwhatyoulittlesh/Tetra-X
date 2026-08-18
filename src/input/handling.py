"""
Tetra-X

File:
    handling.py

Purpose:
    Handles advanced input behaviour.

"""

"""
Note:
    I'm aware about the issue where when you turn cancel_das off,
    it completely ignores DAS and makes it instant, I'm also
    aware that DCD is buggy, and prefer_soft_drop in game.py is a
    bit weird. At the moment I have no fix for any of those, and I
    do not intend on fixing them in this game myself. So unfortunately
    I cannot 100% replicate TETR.IO's handling system, for this version
    of Tetra-X anyways.
"""

from typing import Literal

from constants import MS_PER_FRAME
from settings import Settings


class InputHandler:
    """
    Handles DAS, ARR, DCD and SDF input behaviour.
    """


    def __init__(
        self,
        controls,
        settings: Settings
    ) -> None:

        self.controls = controls
        self.settings = settings


        handling = self.settings.handling


        # ====================
        # TETR.IO Settings
        # ====================

        # Convert frames -> milliseconds

        self.das = (
            handling.das
            * MS_PER_FRAME
        )

        self.arr = (
            handling.arr
            * MS_PER_FRAME
        )

        self.dcd = (
            handling.dcd
            * MS_PER_FRAME
        )

        self.sdf = handling.sdf



        # ====================
        # Horizontal State
        # ====================

        self.direction: Literal[
            "move_left",
            "move_right"
        ] | None = None


        # Last key pressed.
        # Used when both directions are held.

        self.last_pressed: Literal[
            "move_left",
            "move_right"
        ] | None = None



        self.das_timer = {
            "move_left": 0.0,
            "move_right": 0.0
        }

        self.arr_timer = {
            "move_left": 0.0,
            "move_right": 0.0
        }

        self.dcd_timer = 0.0



        self.previous_left = False

        self.previous_right = False




    # ====================
    # Update
    # ====================

    def update(
        self,
        delta_time: float
    ) -> list[str]:

        actions = []


        self.update_dcd(
            delta_time
        )


        self.handle_horizontal(
            delta_time,
            actions
        )


        if self.controls.action_pressed(
            "soft_drop"
        ):

            actions.append(
                "soft_drop"
            )


        return actions




    # ====================
    # DCD
    # ====================

    def update_dcd(
        self,
        delta_time: float
    ) -> None:

        self.dcd_timer = max(
            self.dcd_timer - (delta_time * 1000),
            0
        )



    def reset_handling(self) -> None:
        """
        Resets DAS after lock, rotation or hold.
        """

        for direction in self.das_timer:

            self.das_timer[direction] = 0.0
            self.arr_timer[direction] = 0.0



    def cancel_das(self) -> None:
        """
        Cancels DAS when changing direction.
        """

        if self.direction is None:
            return

        self.das_timer[self.direction] = 0.0
        self.arr_timer[self.direction] = 0.0



    def apply_dcd(self) -> None:
        """
        Applies DAS cut delay.
        """

        self.dcd_timer = self.dcd



    # ====================
    # Horizontal
    # ====================

    def handle_horizontal(
        self,
        delta_time: float,
        actions: list[str]
    ) -> None:


        left = self.controls.action_pressed(
            "move_left"
        )

        right = self.controls.action_pressed(
            "move_right"
        )



        # Detect new presses

        if left and not self.previous_left:

            self.last_pressed = (
                "move_left"
            )


        if right and not self.previous_right:

            self.last_pressed = (
                "move_right"
            )



        self.previous_left = left

        self.previous_right = right



        # ====================
        # Direction Priority
        # ====================

        if left and right:

            direction = self.last_pressed


        elif left:

            direction = "move_left"


        elif right:

            direction = "move_right"


        else:

            direction = None




        # Direction changed

        if direction != self.direction:

            previous_direction = self.direction

            self.direction = direction


            if self.settings.handling.cancel_das:
                self.cancel_das()


            if direction:

                # Direction switch = DCD
                if (
                    previous_direction is not None
                    and self.dcd > 0
                ):

                    self.dcd_timer = self.dcd
                    return
                
                actions.append(direction)



        if direction is None:

            return



        # DCD blocking

        if self.dcd_timer > 0:

            return



        delta_ms = (
            delta_time
            * 1000
        )


        self.das_timer[direction] += delta_ms



        # ====================
        # DAS
        # ====================

        if self.das_timer[direction] < self.das:

            return




        # ====================
        # ARR 0
        # ====================

        if self.arr == 0:

            if self.direction is not None:

                actions.append(
                    self.direction
                    + "_instant"
                )


            self.arr_timer[direction] = 0.0


            return




        # ====================
        # Normal ARR
        # ====================

        self.arr_timer[direction] += delta_ms


        while self.arr_timer[direction] >= self.arr:

            if self.direction is not None:
            
                actions.append(
                    self.direction
                    + "_repeat"
                )


            self.arr_timer[direction] -= self.arr
