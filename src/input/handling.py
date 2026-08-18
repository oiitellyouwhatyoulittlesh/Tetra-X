"""
Tetra-X

File:
    handling.py

Purpose:
    Handles advanced input behaviour.

Note:
    Known limitation: when cancel_das is disabled, DAS is bypassed and defaults to instant.
    DCD behaviour and prefer_soft_drop handling in game.py are also retained as-is for
    this build version.
"""

from typing import Literal

from constants import MS_PER_FRAME
from settings import Settings


class InputHandler:
    """
    Handles DAS, ARR, DCD, and SDF input mechanics.
    """

    def __init__(self, controls, settings: Settings) -> None:
        self.controls = controls
        self.settings = settings

        handling = self.settings.handling

        # Convert frame definitions to milliseconds
        self.das = handling.das * MS_PER_FRAME
        self.arr = handling.arr * MS_PER_FRAME
        self.dcd = handling.dcd * MS_PER_FRAME
        self.sdf = handling.sdf

        # Horizontal state tracking
        self.direction: Literal["move_left", "move_right"] | None = None
        self.last_pressed: Literal["move_left", "move_right"] | None = None

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
    # Core Update
    # ====================

    def update(self, delta_time: float) -> list[str]:
        """
        Updates handling timers and returns list of actions for the current frame.
        """
        actions = []

        self.update_dcd(delta_time)
        self.handle_horizontal(delta_time, actions)

        if self.controls.action_pressed("soft_drop"):
            actions.append("soft_drop")

        return actions


    # ====================
    # Timer & Reset Utilities
    # ====================

    def update_dcd(self, delta_time: float) -> None:
        """
        Decrements active DCD timer.
        """
        self.dcd_timer = max(self.dcd_timer - (delta_time * 1000), 0)


    def reset_handling(self) -> None:
        """
        Resets DAS and ARR timers after piece locking, rotation, or hold.
        """
        for direction in self.das_timer:
            self.das_timer[direction] = 0.0
            self.arr_timer[direction] = 0.0


    def cancel_das(self) -> None:
        """
        Cancels active DAS state when changing directional input.
        """
        if self.direction is None:
            return

        self.das_timer[self.direction] = 0.0
        self.arr_timer[self.direction] = 0.0


    def apply_dcd(self) -> None:
        """
        Applies DAS Cut Delay.
        """
        self.dcd_timer = self.dcd


    # ====================
    # Horizontal Processing
    # ====================

    def handle_horizontal(self, delta_time: float, actions: list[str]) -> None:
        """
        Processes directional input priority, DAS, ARR, and DCD triggers.
        """
        left = self.controls.action_pressed("move_left")
        right = self.controls.action_pressed("move_right")

        # Detect new directional presses
        if left and not self.previous_left:
            self.last_pressed = "move_left"

        if right and not self.previous_right:
            self.last_pressed = "move_right"

        self.previous_left = left
        self.previous_right = right

        # Determine directional priority
        if left and right:
            direction = self.last_pressed
        elif left:
            direction = "move_left"
        elif right:
            direction = "move_right"
        else:
            direction = None

        # Process direction change
        if direction != self.direction:
            previous_direction = self.direction
            self.direction = direction

            if self.settings.handling.cancel_das:
                self.cancel_das()

            if direction:
                # Direction switch triggers DCD
                if previous_direction is not None and self.dcd > 0:
                    self.dcd_timer = self.dcd
                    return

                actions.append(direction)

        if direction is None:
            return

        # Block repeat inputs during active DCD
        if self.dcd_timer > 0:
            return

        delta_ms = delta_time * 1000
        self.das_timer[direction] += delta_ms

        # Check DAS threshold
        if self.das_timer[direction] < self.das:
            return

        # Instant ARR
        if self.arr == 0:
            if self.direction is not None:
                actions.append(self.direction + "_instant")

            self.arr_timer[direction] = 0.0
            return

        # Standard ARR iteration
        self.arr_timer[direction] += delta_ms

        while self.arr_timer[direction] >= self.arr:
            if self.direction is not None:
                actions.append(self.direction + "_repeat")

            self.arr_timer[direction] -= self.arr
