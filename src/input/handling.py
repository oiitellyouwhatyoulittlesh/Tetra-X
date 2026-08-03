"""
Tetra-X

File:
    handling.py

Purpose:
    Handles advanced input behaviour.

"""

from settings import Settings
from typing import Literal


MS_PER_FRAME = 1000.0 / 60.0


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



        self.das_timer = 0.0

        self.arr_timer = 0.0

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

        if self.dcd_timer > 0:

            self.dcd_timer -= (
                delta_time
                * 1000
            )


            if self.dcd_timer < 0:

                self.dcd_timer = 0



    def reset_handling(self) -> None:
        """
        Resets DAS after lock, rotation or hold.
        """

        self.das_timer = 0.0
        self.arr_timer = 0.0



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


            self.das_timer = 0.0
            self.arr_timer = 0.0


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


        self.das_timer += delta_ms



        # ====================
        # DAS
        # ====================

        if self.das_timer < self.das:

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


            self.arr_timer = 0.0


            return




        # ====================
        # Normal ARR
        # ====================

        self.arr_timer += delta_ms


        while self.arr_timer >= self.arr:

            if self.direction is not None:
            
                actions.append(
                    self.direction
                    + "_repeat"
                )


            self.arr_timer -= self.arr
