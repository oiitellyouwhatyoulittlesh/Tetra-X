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
    LOCK_DELAY,
)
from game.board import Board
from game.modes import GameMode
from game.scoring import (
    get_all_clear_score,
    get_hard_drop_score,
    get_line_clear_score,
    get_soft_drop_score,
    get_t_spin_score,
    is_difficult_clear,
)
from input.controls import Controls
from input.handling import InputHandler
from save.records import (
    get_blitz_record,
    get_forty_lines_record,
    update_blitz_record,
    update_forty_lines_record,
)
from settings import Settings


@dataclass
class ClearEvent:
    """
    Stores information about the most recent line clear announcement.
    """

    clear_type: str | None = None
    spin_type: str | None = None
    spin_piece: str | None = None
    combo: int = -1
    all_clear: bool = False
    timer: float = 0.0


class Game:
    """
    Controls the game state and updates.
    """

    # ====================
    # Timing Constants
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
    ZEN_TOP_OUT_TIME = 1.0


    def __init__(self, mode: GameMode) -> None:
        self.mode = mode
        self.settings = Settings()
        self.board = Board()
        self.controls = Controls(self.settings)
        self.input = InputHandler(self.controls, self.settings)

        self.running = True
        self.paused = False
        self.game_over = False

        # Countdown State
        self.countdown = 3.0
        self.countdown_active = False

        # Mode Completion State
        self.completed = False
        self.completion_time = 0.0
        self.results = {}
        self.new_record = False
        self.record_difference = 0

        # Session Statistics
        self.inputs = 0
        self.pieces_placed = 0
        self.lines_cleared = 0
        self.game_time = 0.0

        # Mode Statistics
        self.score = 0
        self.combo = -1
        self.back_to_back = 0
        self.clear_event = ClearEvent()

        self.level = 1
        self.level_lines = 0
        self.level_line_goal = 3

        self.blitz_time = self.BLITZ_TIME

        # Timers
        self.gravity_timer = 0.0
        self.lock_timer = 0.0
        self.lock_resets = 0

        self.soft_drop_timer = 0.0
        self.prevent_hard_drop_timer = 0.0

        self.zen_topout_timer = 0.0
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

        # Countdown Config
        if self.mode in (GameMode.BLITZ, GameMode.FORTY_LINES):
            self.countdown = 3.0
            self.countdown_active = True
        else:
            self.countdown = 0.0
            self.countdown_active = False

        # Completion Reset
        self.completed = False
        self.completion_time = 0.0
        self.results = {}
        self.new_record = False
        self.record_difference = 0

        # Reset Statistics
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

        # Reset Timers
        self.gravity_timer = 0.0
        self.lock_timer = 0.0
        self.lock_resets = 0

        self.soft_drop_timer = 0.0
        self.prevent_hard_drop_timer = 0.0

        self.zen_topout_timer = 0.0


    def restart(self) -> None:
        """
        Restarts the current game session.
        """
        self.start()


    def pause(self) -> None:
        """
        Toggles the pause state.
        """
        self.paused = not self.paused


    # ====================
    # Update Loop
    # ====================

    def update(self, delta_time: float, events) -> None:
        """
        Updates the main game logic and active session state.
        """
        if not self.running:
            return

        # Zen Top Out Freeze
        if self.zen_topout_timer > 0:
            self.zen_topout_timer -= delta_time

            if self.zen_topout_timer <= 0:
                self.zen_topout_timer = 0.0
                self.start()

            return

        # Special Global Event Actions
        actions = self.controls.get_event_actions(events)

        for action in actions:
            if action == "restart":
                self.restart()
                return

            if action == "pause":
                self.pause()
                return

        if self.paused or self.game_over:
            return

        # Countdown Check
        if self.countdown_active:
            self.countdown -= delta_time

            if self.countdown <= 0:
                self.countdown = 0.0
                self.countdown_active = False

            return

        # Session Timer
        self.game_time += delta_time

        # Clear Event Timer
        if self.clear_event.timer > 0:
            self.clear_event.timer -= delta_time

            if self.clear_event.timer <= 0:
                self.clear_event.timer = 0.0
                self.clear_event.clear_type = None
                self.clear_event.spin_type = None
                self.clear_event.spin_piece = None
                self.clear_event.combo = -1
                self.clear_event.all_clear = False

        # Blitz Mode Timer
        if self.mode == GameMode.BLITZ:
            self.blitz_time -= delta_time

            if self.blitz_time <= 0:
                self.blitz_time = 0.0
                self.game_over = True
                self.save_results()
                return

        # Hard Drop Protection Timer
        if self.prevent_hard_drop_timer > 0:
            self.prevent_hard_drop_timer -= delta_time

            if self.prevent_hard_drop_timer < 0:
                self.prevent_hard_drop_timer = 0.0

        # Input & Gravity Handling
        self.handle_input(delta_time, events)
        self.update_gravity(delta_time)

        # Lock Delay Handling
        if not self.board.collision.can_move(self.board.current_piece, 0, 1):
            self.lock_timer += delta_time

            if self.lock_timer >= LOCK_DELAY / FPS:
                if self.settings.handling.prevent_hard_drop:
                    self.prevent_hard_drop_timer = LOCK_DELAY / FPS

                self.lock_piece()
        else:
            self.lock_timer = 0.0


    # ====================
    # Input Handling
    # ====================

    def handle_input(self, delta_time: float, events) -> None:
        """
        Processes continuous and discrete player input actions.
        """
        actions = self.input.update(delta_time)

        if self.settings.handling.prefer_soft_drop and "soft_drop" in actions:
            actions.remove("soft_drop")
            actions.insert(0, "soft_drop")

        # Continuous Actions
        for action in actions:
            if action == "move_left":
                self.move_horizontal(-1)

            elif action == "move_right":
                self.move_horizontal(1)

            elif action in ("move_left_repeat", "move_left_instant"):
                self.move_horizontal(-1, True)

            elif action in ("move_right_repeat", "move_right_instant"):
                self.move_horizontal(1, True)

            elif action == "soft_drop":
                self.soft_drop(delta_time)

        # Count Gameplay Inputs
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
            if event.type == pygame.KEYDOWN and event.key in gameplay_keys:
                self.inputs += 1

        # Discrete Event Actions
        event_actions = self.controls.get_event_actions(events)

        for action in event_actions:
            if action == "hard_drop":
                if (
                    not self.settings.handling.prevent_hard_drop
                    or self.prevent_hard_drop_timer == 0.0
                ):
                    self.hard_drop()

            elif action == "rotate_cw":
                if self.board.rotate_cw():
                    self.last_action_was_rotation = True
                    self.reset_lock_timer_if_grounded()

            elif action == "rotate_ccw":
                if self.board.rotate_ccw():
                    self.last_action_was_rotation = True
                    self.reset_lock_timer_if_grounded()

            elif action == "rotate_180":
                if self.board.rotate_180():
                    self.last_action_was_rotation = True
                    self.reset_lock_timer_if_grounded()

            elif action == "hold":
                self.board.hold()

            elif action == "pause":
                self.pause()

            elif action == "restart":
                self.restart()


    # ====================
    # Gravity Management
    # ====================

    def get_gravity_time(self) -> float:
        """
        Returns the current automatic gravity fall interval based on level.
        """
        index = min(self.level - 1, len(self.GRAVITY_TIMES) - 1)
        return self.GRAVITY_TIMES[index]


    def update_gravity(self, delta_time: float) -> None:
        """
        Handles automatic downward movement via gravity.
        """
        self.gravity_timer += delta_time
        gravity_time = self.get_gravity_time()

        if self.gravity_timer >= gravity_time:
            self.gravity_timer = 0.0
            self.board.move_piece(0, 1)


    # ====================
    # Piece Movement Actions
    # ====================

    def move_horizontal(self, direction: int, repeat: bool = False) -> bool:
        """
        Moves horizontally using active Auto Repeat Rate settings.
        """
        moved = False

        if repeat and self.settings.handling.arr == 0:
            while self.board.move_piece(direction, 0):
                moved = True
        else:
            moved = self.board.move_piece(direction, 0)

        if moved:
            self.last_action_was_rotation = False
            self.reset_lock_timer_if_grounded()

        return moved


    def reset_lock_timer_if_grounded(self) -> None:
        """
        Resets lock delay if the piece is grounded and resets remain under limit.
        """
        if (
            not self.board.collision.can_move(self.board.current_piece, 0, 1)
            and self.lock_resets < 15
        ):
            self.lock_timer = 0.0
            self.lock_resets += 1


    def soft_drop(self, delta_time: float) -> bool:
        """
        Handles soft drop movement based on Soft Drop Factor settings.
        """
        sdf = self.input.sdf

        # Infinite Soft Drop Factor
        if sdf == float("inf"):
            moved_cells = 0
            while self.board.move_piece(0, 1):
                moved_cells += 1

            if moved_cells > 0:
                self.last_action_was_rotation = False
                self.lock_timer = 0.0

                if self.mode == GameMode.BLITZ:
                    self.score += get_soft_drop_score(moved_cells)

            return moved_cells > 0

        # Normal Soft Drop Factor
        if sdf <= 0:
            return False

        self.soft_drop_timer += delta_time
        interval = 1.0 / sdf
        moved_cells = 0

        while self.soft_drop_timer >= interval:
            self.soft_drop_timer -= interval

            if not self.board.move_piece(0, 1):
                break

            moved_cells += 1

        if moved_cells > 0:
            self.last_action_was_rotation = False
            self.lock_timer = 0.0

            if self.mode == GameMode.BLITZ:
                self.score += get_soft_drop_score(moved_cells)

        return moved_cells > 0


    def hard_drop(self) -> None:
        """
        Drops the piece instantly and applies score based on drop height.
        """
        dropped_cells = 0

        while self.board.move_piece(0, 1):
            dropped_cells += 1

        if dropped_cells > 0 and self.mode == GameMode.BLITZ:
            self.score += get_hard_drop_score(dropped_cells)

        self.lock_piece()


    # ====================
    # Clear Tracking & Scoring
    # ====================

    def update_clear_chain(
        self,
        cleared: int,
        spin_type: str | None,
        all_clear: bool
    ) -> None:
        """
        Updates combo and Back-to-Back streak states.
        """
        if cleared == 0:
            self.combo = -1
        else:
            self.combo += 1

        difficult_clear = is_difficult_clear(cleared, spin_type, all_clear)

        if difficult_clear:
            self.back_to_back += 1
        elif cleared > 0:
            self.back_to_back = 0


    def add_line_clear_score(
        self,
        cleared: int,
        spin_type: str | None = None,
        all_clear: bool = False
    ) -> None:
        """
        Calculates and adds score awarded for a line clear in Blitz mode.
        """
        if self.mode != GameMode.BLITZ:
            return

        # Base Clear Score
        if spin_type == "T-SPIN":
            score = get_t_spin_score(cleared, self.level, False)
        elif spin_type == "MINI":
            score = get_t_spin_score(cleared, self.level, True)
        else:
            score = get_line_clear_score(cleared, self.level)

        # All Clear Bonus
        if all_clear:
            score += get_all_clear_score(self.level)

        # Combo Bonus
        if self.combo > 0:
            score += 50 * self.combo * self.level

        # Back-to-Back Multiplier
        if self.back_to_back > 1:
            score = int(score * 1.5)

        self.score += score


    def lock_piece(self) -> None:
        """
        Locks the current active piece and updates playfield clears and scores.
        """
        if self.board.current_piece is None:
            return

        # Spin Detection
        spin_type = self.board.get_spin_type(self.last_action_was_rotation)
        t_spin = (spin_type == "T-SPIN")
        mini_spin = (spin_type == "MINI")

        spin_piece = (
            self.board.current_piece.type
            if spin_type is not None
            else None
        )

        # Lock and Clear
        self.board.lock_piece()
        cleared = self.board.clear_lines()

        # All Clear Check
        all_clear = (cleared > 0 and self.board.is_all_clear())

        # Update Clear Chain & Scoring
        self.update_clear_chain(cleared, spin_type, all_clear)

        if self.mode == GameMode.BLITZ:
            self.add_line_clear_score(cleared, spin_type, all_clear)

        # Set Announcement Event
        if cleared > 0 or all_clear or spin_type is not None:
            self.clear_event = ClearEvent(
                clear_type=self.get_clear_name(cleared),
                spin_type=(
                    "T-SPIN"
                    if t_spin
                    else (
                        f"MINI {spin_piece}-SPIN"
                        if mini_spin
                        else None
                    )
                ),
                spin_piece=spin_piece,
                combo=self.combo if cleared > 0 else -1,
                all_clear=all_clear,
                timer=self.CLEAR_EVENT_TIME
            )

        # Update Session Totals
        self.pieces_placed += 1
        self.lines_cleared += cleared

        # 40 Lines Victory Check
        if self.mode == GameMode.FORTY_LINES and self.lines_cleared >= 40:
            self.lines_cleared = 40
            self.completion_time = self.game_time
            self.completed = True
            self.game_over = True
            self.save_results()
            return

        # Blitz Level Progression
        if self.mode == GameMode.BLITZ:
            self.level_lines += cleared
            while self.level_lines >= self.level_line_goal:
                self.level_lines -= self.level_line_goal
                self.level += 1
                self.level_line_goal += 2

        # Spawn Next Piece
        self.lock_timer = 0.0
        self.lock_resets = 0

        if not self.board.spawn_piece():
            if self.mode == GameMode.ZEN:
                self.zen_topout_timer = self.ZEN_TOP_OUT_TIME
            else:
                self.game_over = True

        self.input.reset_handling()
        self.soft_drop_timer = 0.0
        self.last_action_was_rotation = False


    # ====================
    # Results & Records
    # ====================

    def create_results(self) -> dict:
        """
        Generates a summary dictionary of session statistics.
        """
        pieces = self.pieces_placed
        inputs_per_piece = (self.inputs / pieces if pieces > 0 else 0.0)

        display_time = (
            self.completion_time
            if self.mode == GameMode.FORTY_LINES and self.completed
            else self.game_time
        )

        pieces_per_second = (pieces / display_time if display_time > 0 else 0.0)

        return {
            "score": self.score,
            "lines": self.lines_cleared,
            "pieces": pieces,
            "pps": pieces_per_second,
            "inputs": self.inputs,
            "inputs_per_piece": inputs_per_piece,
            "time": display_time,
            "level": self.level
        }


    def save_results(self) -> None:
        """
        Saves current results if a personal record was set.
        """
        self.results = self.create_results()
        self.new_record = False
        self.record_difference = 0

        if self.mode == GameMode.BLITZ:
            record = get_blitz_record()
            old_score = record["score"]
            self.record_difference = self.results["score"] - old_score
            self.new_record = update_blitz_record(self.results)

        elif self.mode == GameMode.FORTY_LINES:
            record = get_forty_lines_record()
            old_time = record["time"]

            if old_time is None:
                self.record_difference = 0
            else:
                self.record_difference = self.results["time"] - old_time

            self.new_record = update_forty_lines_record(self.results)


    # ====================
    # Statistics & Utilities
    # ====================

    def get_inputs_per_piece(self) -> float:
        """
        Returns average key inputs performed per piece.
        """
        if self.pieces_placed == 0:
            return 0.0

        return self.inputs / self.pieces_placed


    def get_pieces_per_second(self) -> float:
        """
        Returns pieces placed per second rate.
        """
        if self.game_time <= 0:
            return 0.0

        return self.pieces_placed / self.game_time


    def get_clear_name(self, cleared: int) -> str | None:
        """
        Returns display text for cleared line count.
        """
        names = {
            1: "SINGLE",
            2: "DOUBLE",
            3: "TRIPLE",
            4: "QUAD"
        }
        return names.get(cleared)


    def get_board(self) -> Board:
        """
        Returns the active board instance.
        """
        return self.board
