"""
Tetra-X

File:
    game.py

Purpose:
    Controls the main game logic.

"""

from constants import (
    FPS,
    LOCK_DELAY
)

from game.board import Board

from input.controls import Controls
from input.handling import InputHandler

from settings import Settings

class Game:
    """
    Controls the game state and updates.
    """

    # ====================
    # Timing
    # ====================

    GRAVITY_TIME = 1.0


    def __init__(self) -> None:

        self.settings = Settings()

        self.board = Board()

        self.controls = Controls()

        self.input = InputHandler(
            self.controls,
            self.settings
        )


        self.running = True
        self.paused = False
        self.game_over = False

        self.gravity_timer = 0.0
        self.lock_timer = 0.0
        self.lock_resets = 0

        self.soft_drop_timer = 0.0
        self.prevent_hard_drop_timer = 0.0


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

        if self.paused:
            return

        if self.game_over:
            return


        if self.prevent_hard_drop_timer > 0:

            self.prevent_hard_drop_timer -= delta_time

            if self.prevent_hard_drop_timer < 0:

                self.prevent_hard_drop_timer = 0.0


        self.handle_input(
            delta_time,
            events
        )


        self.update_gravity(
            delta_time
        )


        if not self.board.collision.can_move(
            self.board.current_piece,
            0,
            1
        ):

            self.lock_timer += delta_time


            if self.lock_timer >= LOCK_DELAY / FPS:

                if self.settings.handling.prevent_hard_drop:

                    self.prevent_hard_drop_timer = LOCK_DELAY / FPS

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



        actions = self.controls.get_event_actions(events)


        for event in actions:


            if event == "hard_drop":

                if (
                    not self.settings.handling.prevent_hard_drop
                    or self.prevent_hard_drop_timer == 0.0
                ):

                    self.hard_drop()


            elif event == "rotate_cw":

                rotated = self.board.rotate_cw()

                if rotated:
                    self.reset_lock_timer_if_grounded()


            elif event == "rotate_ccw":

                rotated = self.board.rotate_ccw()

                if rotated:
                    self.reset_lock_timer_if_grounded()


            elif event == "rotate_180":

                rotated = self.board.rotate_180()

                if rotated:
                    self.reset_lock_timer_if_grounded()

            elif event == "hold":

                self.board.hold()

            elif event == "pause":

                self.pause()


            elif event == "restart":

                self.restart()



    # ====================
    # Gravity
    # ====================

    def update_gravity(
        self,
        delta_time: float
    ) -> None:
        """
        Handles automatic falling.
        """

        self.gravity_timer += delta_time


        if self.gravity_timer >= self.GRAVITY_TIME:

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


        if repeat and self.settings.handling.arr == 0:

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
    
    
        # Infinite SDF
    
        if sdf == float("inf"):
    
            moved = False
    
            while self.board.move_piece(
                0,
                1
            ):
                moved = True
    
    
            if moved:
    
                self.lock_timer = 0.0
    
    
            return moved
    
    
    
        # Normal SDF
    
        if sdf <= 0:
    
            return False
    
    
    
        self.soft_drop_timer += (
            delta_time
        )
    
    
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



    def lock_piece(self) -> None:
        """
        Locks the current piece.
        """

        self.board.lock_piece()

        self.board.clear_lines()

        self.lock_timer = 0.0

        self.lock_resets = 0


        if not self.board.spawn_piece():

            self.game_over = True
        

        self.input.reset_handling()

        self.soft_drop_timer = 0.0



    # ====================
    # Information
    # ====================

    def get_board(self) -> Board:
        """
        Returns the current board.
        """

        return self.board
