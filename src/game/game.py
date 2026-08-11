"""
Tetra-X

File:
    game.py

Purpose:
    Controls the main game logic.

"""

from dataclasses import dataclass
import pygame

from constants import (
    FPS,
    LOCK_DELAY
)

from game.board import Board

from input.controls import Controls
from input.handling import InputHandler

from settings import Settings
from game.modes import GameMode
from game.scoring import (
    get_line_clear_score,
    get_t_spin_score,
    get_perfect_clear_score,
    is_difficult_clear
)


@dataclass
class ClearEvent:
    """
    Stores information about the most recent line clear announcement.
    """

    clear_type: str | None = None
    spin_type: str | None = None
    spin_piece: str | None = None
    combo: int = -1
    perfect_clear: bool = False
    timer: float = 0.0


class Game:
    """
    Controls the game state and updates.
    """

    # ====================
    # Timing
    # ====================

    GRAVITY_TIMES = (
        1.000,
        0.850,
        0.700,
        0.550,
        0.425,
        0.325,
        0.250,
        0.190,
        0.140,
        0.100,
        0.075
    )

    BLITZ_TIME = 120.0
    CLEAR_EVENT_TIME = 2.0


    def __init__(
        self,
        mode: GameMode
    ) -> None:

        self.mode = mode

        self.settings = Settings()

        self.board = Board()

        self.controls = Controls(
            self.settings
        )

        self.input = InputHandler(
            self.controls,
            self.settings
        )


        self.running = True
        self.paused = False
        self.game_over = False


        # ====================
        # Countdown State
        # ====================

        self.countdown = 3.0
        self.countdown_active = False


        # ====================
        # 40L / Mode Completion State
        # ====================

        self.completed = False
        self.completion_time = 0.0


        # ====================
        # Session Statistics
        # ====================

        self.inputs = 0
        self.pieces_placed = 0
        self.lines_cleared = 0
        self.game_time = 0.0


        # ====================
        # Mode Statistics
        # ====================

        self.score = 0

        self.combo = -1
        self.back_to_back = 0
        self.clear_event = ClearEvent()

        self.level = 1
        self.level_lines = 0
        self.level_line_goal = 3

        self.blitz_time = self.BLITZ_TIME


        # ====================
        # Timers
        # ====================

        self.gravity_timer = 0.0
        self.lock_timer = 0.0
        self.lock_resets = 0

        self.soft_drop_timer = 0.0
        self.prevent_hard_drop_timer = 0.0

        self.last_action_was_rotation = False


    # ====================
    # Game Control
    # ====================

    def start(self) -> None:
        """
        Starts a new game.
        """

        self.board.reset()

        self.running = True
        self.paused = False
        self.game_over = False

        self.last_action_was_rotation = False


        # ====================
        # Countdown Config
        # ====================

        if self.mode in (GameMode.BLITZ, GameMode.FORTY_LINES):
            self.countdown = 3.0
            self.countdown_active = True
        else:
            self.countdown = 0.0
            self.countdown_active = False


        # ====================
        # Completion Reset
        # ====================

        self.completed = False
        self.completion_time = 0.0


        # ====================
        # Reset Statistics
        # ====================

        self.inputs = 0
        self.pieces_placed = 0
        self.lines_cleared = 0
        self.game_time = 0.0

        self.score = 0

        self.combo = -1
        self.back_to_back = 0
        self.clear_event = ClearEvent()

        self.level = 1
        self.level_lines = 0
        self.level_line_goal = 3

        self.blitz_time = self.BLITZ_TIME


        # ====================
        # Reset Timers
        # ====================

        self.gravity_timer = 0.0
        self.lock_timer = 0.0
        self.lock_resets = 0

        self.soft_drop_timer = 0.0
        self.prevent_hard_drop_timer = 0.0


    def restart(self) -> None:
        """
        Restarts the current game.
        """

        self.start()


    def pause(self) -> None:
        """
        Toggles pause state.
        """

        self.paused = not self.paused


    # ====================
    # Update
    # ====================

    def update(
        self,
        delta_time: float,
        events
    ) -> None:
        """
        Updates the game logic.
        """

        if not self.running:
            return
        

        # ====================
        # Special Input
        # ====================

        actions = self.controls.get_event_actions(
            events
        )


        for action in actions:

            if action == "restart":

                self.restart()
                return


            if action == "pause":

                self.pause()
                return


        if self.paused:
            return

        if self.game_over:
            return


        # ====================
        # Countdown Check
        # ====================

        if self.countdown_active:

            self.countdown -= delta_time

            if self.countdown <= 0:

                self.countdown = 0.0
                self.countdown_active = False

            return


        # ====================
        # Session Timer
        # ====================

        self.game_time += delta_time


        # ====================
        # Clear Event Timer
        # ====================

        if self.clear_event.timer > 0:

            self.clear_event.timer -= delta_time

            if self.clear_event.timer <= 0:

                self.clear_event.timer = 0.0
                self.clear_event.clear_type = None
                self.clear_event.spin_type = None
                self.clear_event.spin_piece = None
                self.clear_event.combo = -1
                self.clear_event.perfect_clear = False


        # ====================
        # Blitz Timer
        # ====================

        if self.mode == GameMode.BLITZ:

            self.blitz_time -= delta_time

            if self.blitz_time <= 0:

                self.blitz_time = 0.0
                self.game_over = True

                return


        # ====================
        # Hard Drop Protection
        # ====================

        if self.prevent_hard_drop_timer > 0:

            self.prevent_hard_drop_timer -= delta_time

            if self.prevent_hard_drop_timer < 0:

                self.prevent_hard_drop_timer = 0.0


        # ====================
        # Input
        # ====================

        self.handle_input(
            delta_time,
            events
        )


        # ====================
        # Gravity
        # ====================

        self.update_gravity(
            delta_time
        )


        # ====================
        # Lock Delay
        # ====================

        if not self.board.collision.can_move(
            self.board.current_piece,
            0,
            1
        ):

            self.lock_timer += delta_time


            if self.lock_timer >= LOCK_DELAY / FPS:

                if self.settings.handling.prevent_hard_drop:

                    self.prevent_hard_drop_timer = (
                        LOCK_DELAY / FPS
                    )

                self.lock_piece()


        else:

            self.lock_timer = 0.0


    # ====================
    # Input
    # ====================

    def handle_input(
        self,
        delta_time: float,
        events
    ) -> None:
        """
        Handles player actions.
        """

        actions = self.input.update(
            delta_time
        )


        if (
            self.settings.handling.prefer_soft_drop
            and "soft_drop" in actions
        ):

            actions.remove(
                "soft_drop"
            )

            actions.insert(
                0,
                "soft_drop"
            )


        # ====================
        # Continuous Input
        # ====================

        for action in actions:

            if action == "move_left":

                self.move_horizontal(
                    -1
                )


            elif action == "move_right":

                self.move_horizontal(
                    1
                )


            elif action == "move_left_repeat":

                self.move_horizontal(
                    -1,
                    True
                )


            elif action == "move_right_repeat":

                self.move_horizontal(
                    1,
                    True
                )


            elif action == "move_left_instant":

                self.move_horizontal(
                    -1,
                    True
                )


            elif action == "move_right_instant":

                self.move_horizontal(
                    1,
                    True
                )


            elif action == "soft_drop":

                self.soft_drop(
                    delta_time
                )


        # ====================
        # Count Gameplay Inputs
        # ====================

        gameplay_actions = (
            "move_left",
            "move_right",
            "soft_drop",
            "hard_drop",
            "rotate_cw",
            "rotate_ccw",
            "rotate_180",
            "hold"
        )

        gameplay_keys = {
            self.controls.get_binding(action)
            for action in gameplay_actions
        }

        gameplay_keys.discard(None)

        for event in events:

            if event.type != pygame.KEYDOWN:
                continue

            if event.key in gameplay_keys:

                self.inputs += 1


        # ====================
        # Key Events
        # ====================

        actions = self.controls.get_event_actions(
            events
        )


        for action in actions:

            if action == "hard_drop":

                if (
                    not self.settings.handling.prevent_hard_drop
                    or self.prevent_hard_drop_timer == 0.0
                ):

                    self.hard_drop()


            elif action == "rotate_cw":

                rotated = self.board.rotate_cw()

                if rotated:

                    self.last_action_was_rotation = True
                    self.reset_lock_timer_if_grounded()


            elif action == "rotate_ccw":

                rotated = self.board.rotate_ccw()

                if rotated:

                    self.last_action_was_rotation = True
                    self.reset_lock_timer_if_grounded()


            elif action == "rotate_180":

                rotated = self.board.rotate_180()

                if rotated:

                    self.last_action_was_rotation = True
                    self.reset_lock_timer_if_grounded()


            elif action == "hold":

                self.board.hold()


            elif action == "pause":

                self.pause()


            elif action == "restart":

                self.restart()


    # ====================
    # Gravity
    # ====================

    def get_gravity_time(self) -> float:
        """
        Returns the current automatic gravity interval.
        """

        index = min(
            self.level - 1,
            len(self.GRAVITY_TIMES) - 1
        )

        return self.GRAVITY_TIMES[index]


    def update_gravity(
        self,
        delta_time: float
    ) -> None:
        """
        Handles automatic falling.
        """

        self.gravity_timer += delta_time

        gravity_time = self.get_gravity_time()

        if self.gravity_timer >= gravity_time:

            self.gravity_timer = 0.0

            self.board.move_piece(
                0,
                1
            )


    # ====================
    # Piece Actions
    # ====================

    def move_horizontal(
        self,
        direction: int,
        repeat: bool = False
    ) -> bool:
        """
        Moves horizontally using the current ARR settings.
        """

        moved = False


        if (
            repeat
            and self.settings.handling.arr == 0
        ):

            while self.board.move_piece(
                direction,
                0
            ):

                moved = True

        else:

            moved = self.board.move_piece(
                direction,
                0
            )


        if moved:

            self.last_action_was_rotation = False
            self.reset_lock_timer_if_grounded()


        return moved


    def reset_lock_timer_if_grounded(self) -> None:
        """
        Resets lock delay if the piece is touching the ground.
        """

        if not self.board.collision.can_move(
            self.board.current_piece,
            0,
            1
        ):

            if self.lock_resets < 15:

                self.lock_timer = 0.0
                self.lock_resets += 1


    def soft_drop(
        self,
        delta_time: float
    ) -> bool:
        """
        Handles soft drop speed.
        """

        sdf = self.input.sdf


        # ====================
        # Infinite SDF
        # ====================

        if sdf == float("inf"):

            moved = False


            while self.board.move_piece(
                0,
                1
            ):

                moved = True


            if moved:

                self.last_action_was_rotation = False
                self.lock_timer = 0.0


            return moved


        # ====================
        # Normal SDF
        # ====================

        if sdf <= 0:

            return False


        self.soft_drop_timer += delta_time


        interval = (
            1.0 / sdf
        )


        moved = False


        while self.soft_drop_timer >= interval:

            self.soft_drop_timer -= interval


            if not self.board.move_piece(
                0,
                1
            ):

                break


            moved = True


        if moved:

            self.last_action_was_rotation = False
            self.lock_timer = 0.0


        return moved


    def hard_drop(self) -> None:
        """
        Drops the piece instantly.
        """

        while self.board.move_piece(
            0,
            1
        ):

            pass


        self.lock_piece()


    # ====================
    # Clear Tracking & Scoring
    # ====================

    def update_clear_chain(
            self,
            cleared: int,
            spin_type: str | None,
            perfect_clear: bool
        ) -> None:
            """
            Updates combo and Back-to-Back state.
            """

            if cleared == 0:
                self.combo = -1
            else:
                self.combo += 1

            difficult_clear = is_difficult_clear(
                cleared,
                spin_type,
                perfect_clear
            )

            # ====================
            # Perfect Clear / Difficult Clear
            # ====================

            if perfect_clear:
                self.back_to_back += 2

            elif difficult_clear:
                self.back_to_back += 1

            elif cleared > 0:
                self.back_to_back = 0


    def add_line_clear_score(
        self,
        cleared: int,
        spin_type: str | None = None,
        perfect_clear: bool = False
    ) -> None:
        """
        Adds score for a line clear.
        """

        if self.mode != GameMode.BLITZ:
            return


        # ====================
        # Base Clear Score
        # ====================

        if spin_type == "T-SPIN":

            score = get_t_spin_score(
                cleared,
                self.level,
                False
            )

        elif spin_type == "MINI":

            score = get_t_spin_score(
                cleared,
                self.level,
                True
            )

        else:

            score = get_line_clear_score(
                cleared,
                self.level
            )


        # ====================
        # Perfect Clear
        # ====================

        if perfect_clear:

            score += get_perfect_clear_score(
                self.level
            )


        # ====================
        # Combo
        # ====================

        if self.combo > 0:

            score += (
                50
                * self.combo
                * self.level
            )


        # ====================
        # B2B
        # ====================

        if self.back_to_back > 1:

            score = int(
                score * 1.5
            )


        self.score += score


    def lock_piece(self) -> None:
        """
        Locks the current piece and updates clear state.
        """

        if self.board.current_piece is None:
            return


        # ====================
        # Spin Detection
        # ====================

        spin_type = self.board.get_spin_type(
            self.last_action_was_rotation
        )

        t_spin = (
            spin_type == "T-SPIN"
        )

        mini_spin = (
            spin_type == "MINI"
        )


        spin_piece = (
            self.board.current_piece.type
            if spin_type is not None
            else None
        )


        # ====================
        # Lock
        # ====================

        self.board.lock_piece()

        cleared = self.board.clear_lines()


        # ====================
        # Perfect Clear
        # ====================

        perfect_clear = (
            cleared > 0
            and self.board.is_perfect_clear()
        )


        # ====================
        # Clear Chain
        # ====================

        self.update_clear_chain(
            cleared,
            spin_type,
            perfect_clear
        )


        # ====================
        # Scoring
        # ====================

        if self.mode == GameMode.BLITZ:

            self.add_line_clear_score(
                cleared,
                spin_type,
                perfect_clear
            )


        # ====================
        # Clear Event
        # ====================

        if (
            cleared > 0
            or perfect_clear
        ):

            self.clear_event = ClearEvent(

                clear_type=self.get_clear_name(
                    cleared
                ),

                spin_type=(
                    "T-SPIN"
                    if t_spin
                    else (
                        "MINI SPIN"
                        if mini_spin
                        else None
                    )
                ),

                spin_piece=spin_piece,

                combo=self.combo,

                perfect_clear=perfect_clear,

                timer=self.CLEAR_EVENT_TIME
            )


        # ====================
        # Statistics
        # ====================

        self.pieces_placed += 1
        self.lines_cleared += cleared


        # ====================
        # 40 Lines Check
        # ====================

        if self.mode == GameMode.FORTY_LINES:

            if self.lines_cleared >= 40:

                self.lines_cleared = 40
                self.completion_time = self.game_time
                self.completed = True
                self.game_over = True

                return


        # ====================
        # Blitz Level
        # ====================

        if self.mode == GameMode.BLITZ:

            self.level_lines += cleared

            while (
                self.level_lines
                >= self.level_line_goal
            ):

                self.level_lines -= (
                    self.level_line_goal
                )

                self.level += 1

                self.level_line_goal += 2


        # ====================
        # Next Piece
        # ====================

        self.lock_timer = 0.0
        self.lock_resets = 0


        if not self.board.spawn_piece():

            self.game_over = True


        self.input.reset_handling()

        self.soft_drop_timer = 0.0

        self.last_action_was_rotation = False


    # ====================
    # Statistics
    # ====================

    def get_inputs_per_piece(self) -> float:
        """
        Returns the average number of inputs per piece.
        """

        if self.pieces_placed == 0:

            return 0.0

        return (
            self.inputs
            / self.pieces_placed
        )


    def get_pieces_per_second(self) -> float:
        """
        Returns the current pieces per second.
        """

        if self.game_time <= 0:

            return 0.0

        return (
            self.pieces_placed
            / self.game_time
        )


    # ====================
    # Clear Names
    # ====================

    def get_clear_name(
        self,
        cleared: int
    ) -> str | None:
        """
        Returns the display name for a line clear.
        """

        names = {
            1: "SINGLE",
            2: "DOUBLE",
            3: "TRIPLE",
            4: "QUAD"
        }

        return names.get(
            cleared
        )


    # ====================
    # Information
    # ====================

    def get_board(self) -> Board:
        """
        Returns the current board.
        """

        return self.board
