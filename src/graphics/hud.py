"""
Tetra-X

File:
    hud.py

Purpose:
    Draws the game's HUD.

"""

import pygame

from constants import (
    CELL_SIZE,
    BOARD_COLUMNS,
    GRID
)

from game.pieces import (
    get_cells,
    get_colour
)

from game.modes import GameMode


class HUD:
    """
    Draws the game HUD.
    """

    PANEL_WIDTH = 6 * CELL_SIZE

    HOLD_HEIGHT = 4 * CELL_SIZE
    NEXT_HEIGHT = 16 * CELL_SIZE

    GAP = 40
    CORNER = 20
    MINI_CELL_SIZE = 30


    def __init__(self) -> None:
        """
        Creates HUD resources.
        """

        self.font = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )

        self.stat_font = pygame.font.SysFont(
            "Arial",
            22,
            bold=True
        )

        self.value_font = pygame.font.SysFont(
            "Arial",
            22
        )


    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        screen,
        game,
        board_x: int,
        board_y: int
    ) -> None:
        """
        Draws the HUD.
        """

        board = game.get_board()

        board_width = (
            BOARD_COLUMNS * CELL_SIZE
        )


        hold_x = (
            board_x
            - self.GAP
            - self.PANEL_WIDTH
        )

        next_x = (
            board_x
            + board_width
            + self.GAP
        )


        self.draw_hold_panel(
            screen,
            board,
            hold_x,
            board_y
        )

        self.draw_next_panel(
            screen,
            board,
            next_x,
            board_y
        )

        self.draw_game_stats(
            screen,
            game,
            board_x,
            board_y,
            board_width
        )


    # ====================
    # Panels
    # ====================

    def draw_hold_panel(
        self,
        screen,
        board,
        x: int,
        y: int
    ) -> None:
        """
        Draws the hold panel.
        """

        rectangle = pygame.Rect(
            x,
            y,
            self.PANEL_WIDTH,
            self.HOLD_HEIGHT
        )


        pygame.draw.rect(
            screen,
            GRID,
            rectangle,
            2
        )


        pygame.draw.line(
            screen,
            GRID,
            (
                x,
                y + self.HOLD_HEIGHT
            ),
            (
                x + self.CORNER,
                y + self.HOLD_HEIGHT - self.CORNER
            ),
            2
        )


        self.draw_label(
            screen,
            "HOLD",
            x,
            y - 32
        )


        if board.held_piece is not None:

            self.draw_mini_piece(
                screen,
                board.held_piece,
                x + self.PANEL_WIDTH // 2,
                y + self.HOLD_HEIGHT // 2
            )


    # ====================
    # Mini Pieces
    # ====================

    def draw_mini_piece(
        self,
        screen,
        piece: str,
        center_x: int,
        center_y: int
    ) -> None:
        """
        Draws a miniature piece centred at a position.
        """

        cells = get_cells(
            piece,
            0
        )

        colour = get_colour(
            piece
        )


        min_x = min(
            x for x, _ in cells
        )

        max_x = max(
            x for x, _ in cells
        )

        min_y = min(
            y for _, y in cells
        )

        max_y = max(
            y for _, y in cells
        )


        width = (
            max_x - min_x + 1
        ) * self.MINI_CELL_SIZE

        height = (
            max_y - min_y + 1
        ) * self.MINI_CELL_SIZE


        start_x = (
            center_x
            - width // 2
        )

        start_y = (
            center_y
            - height // 2
        )


        for cell_x, cell_y in cells:

            x = (
                start_x
                + (cell_x - min_x)
                * self.MINI_CELL_SIZE
            )

            y = (
                start_y
                + (cell_y - min_y)
                * self.MINI_CELL_SIZE
            )


            rectangle = pygame.Rect(
                x,
                y,
                self.MINI_CELL_SIZE,
                self.MINI_CELL_SIZE
            )


            pygame.draw.rect(
                screen,
                colour,
                rectangle.inflate(
                    -2,
                    -2
                )
            )


    def draw_next_panel(
        self,
        screen,
        board,
        x: int,
        y: int
    ) -> None:
        """
        Draws the next panel.
        """

        preview = board.get_preview()

        top_margin = 55
        bottom_margin = 35

        usable_height = (
            self.NEXT_HEIGHT
            - top_margin
            - bottom_margin
        )

        spacing = usable_height / 5


        for index, piece in enumerate(
            preview[:5]
        ):

            center_y = (
                y
                + top_margin
                + spacing * index
                + spacing / 2
            )

            self.draw_mini_piece(
                screen,
                piece,
                x + self.PANEL_WIDTH // 2,
                int(center_y)
            )


        rectangle = pygame.Rect(
            x,
            y,
            self.PANEL_WIDTH,
            self.NEXT_HEIGHT
        )


        pygame.draw.rect(
            screen,
            GRID,
            rectangle,
            2
        )


        pygame.draw.line(
            screen,
            GRID,
            (
                x + self.PANEL_WIDTH,
                y + self.NEXT_HEIGHT
            ),
            (
                x + self.PANEL_WIDTH - self.CORNER,
                y + self.NEXT_HEIGHT - self.CORNER
            ),
            2
        )


        self.draw_label(
            screen,
            "NEXT",
            x,
            y - 32
        )


    # ====================
    # Text
    # ====================

    def draw_label(
        self,
        screen,
        text: str,
        x: int,
        y: int
    ) -> None:
        """
        Draws a HUD label.
        """

        surface = self.font.render(
            text,
            True,
            GRID
        )

        screen.blit(
            surface,
            (
                x,
                y
            )
        )


    # ====================
    # Game Stats
    # ====================

    def draw_game_stats(
        self,
        screen,
        game,
        board_x: int,
        board_y: int,
        board_width: int
    ) -> None:
        """
        Draws the game statistics based on
        the current game mode.
        """

        right_align_x = (
            board_x
            - self.GAP
        )

        bottom_y = (
            screen.get_height()
            - 460
        )


        label_colour = (
            255,
            255,
            255
        )

        value_colour = (
            255,
            255,
            255
        )


        # ====================
        # Mode Specific Stats
        # ====================

        if game.mode == GameMode.BLITZ:

            total_milliseconds = int(
                game.blitz_time * 1000
            )

            minutes = (
                total_milliseconds // 60000
            )

            seconds = (
                total_milliseconds // 1000
            ) % 60

            milliseconds = (
                total_milliseconds % 1000
            )

            time_text = (
                f"{minutes}:"
                f"{seconds:02d}."
                f"{milliseconds:03d}"
            )


            stats = [
                (
                    "SCORE",
                    f"{game.score:,}"
                ),

                (
                    "TIME",
                    time_text
                ),

                (
                    "LEVEL",
                    str(game.level)
                ),

                (
                    "LINES",
                    f"{game.level_lines} / {game.level_line_goal}"
                )
            ]


        elif game.mode == GameMode.FORTY_LINES:

            display_time = (
                game.completion_time
                if game.completed
                else game.game_time
            )


            total_milliseconds = int(
                display_time * 1000
            )

            minutes = (
                total_milliseconds // 60000
            )

            seconds = (
                total_milliseconds // 1000
            ) % 60

            milliseconds = (
                total_milliseconds % 1000
            )


            time_text = (
                f"{minutes}:"
                f"{seconds:02d}."
                f"{milliseconds:03d}"
            )


            inputs = game.inputs
            pieces = game.pieces_placed


            inputs_per_piece = (
                inputs / pieces
                if pieces > 0
                else 0.0
            )


            pieces_per_second = (
                pieces / display_time
                if display_time > 0
                else 0.0
            )


            stats = [
                (
                    "LINES",
                    f"{game.lines_cleared} / 40"
                ),

                (
                    "TIME",
                    time_text
                ),

                (
                    "PIECES",
                    f"{pieces}, "
                    f"{pieces_per_second:.2f}/S"
                ),

                (
                    "INPUTS",
                    f"{inputs}, "
                    f"{inputs_per_piece:.2f}/P"
                )
            ]


        else:

            # ====================
            # Zen / Standard
            # ====================

            inputs = game.inputs
            pieces = game.pieces_placed


            inputs_per_piece = (
                inputs / pieces
                if pieces > 0
                else 0.0
            )


            pieces_per_second = (
                pieces / game.game_time
                if game.game_time > 0
                else 0.0
            )


            total_milliseconds = int(
                game.game_time * 1000
            )

            minutes = (
                total_milliseconds // 60000
            )

            seconds = (
                total_milliseconds // 1000
            ) % 60

            milliseconds = (
                total_milliseconds % 1000
            )


            time_text = (
                f"{minutes}:"
                f"{seconds:02d}."
                f"{milliseconds:03d}"
            )


            stats = [
                (
                    "INPUTS",
                    f"{inputs}, "
                    f"{inputs_per_piece:.2f}/P"
                ),

                (
                    "PIECES",
                    f"{pieces}, "
                    f"{pieces_per_second:.2f}/S"
                ),

                (
                    "LINES",
                    str(game.lines_cleared)
                ),

                (
                    "TIME",
                    time_text
                )
            ]


        # ====================
        # Dynamic Clear Event Area
        # ====================

        hold_bottom = (
            board_y
            + self.HOLD_HEIGHT
        )

        stats_top = bottom_y

        middle_space = (
            stats_top
            - hold_bottom
        )

        event_height = (
            self.get_clear_event_height(
                game
            )
        )

        event_y = (
            hold_bottom
            + middle_space // 2
            - event_height // 2
        )


        self.draw_clear_event(
            screen,
            game,
            right_align_x,
            event_y
        )


        # ====================
        # Render Stats
        # ====================

        line_height = 42

        y = bottom_y


        for label, value in stats:

            label_surface = self.stat_font.render(
                label,
                True,
                label_colour
            )

            value_surface = self.value_font.render(
                value,
                True,
                value_colour
            )


            label_rect = label_surface.get_rect(
                right=right_align_x,
                y=y
            )

            value_rect = value_surface.get_rect(
                right=right_align_x,
                y=y + 22
            )


            screen.blit(
                label_surface,
                label_rect
            )

            screen.blit(
                value_surface,
                value_rect
            )


            y += line_height + 22


    # ====================
    # Clear Event
    # ====================

    def draw_clear_event(
        self,
        screen,
        game,
        right_align_x: int,
        y: int
    ) -> None:
        """
        Draws the temporary line-clear announcement and persistent B2B state.
        """

        event = game.clear_event

        items = []

        display_b2b = max(
            game.back_to_back - 1,
            0
        )

        if event.timer > 0:

            # ====================
            # Spin
            # ====================

            if event.spin_type is not None:

                spin_color = (
                    get_colour(event.spin_piece)
                    if event.spin_piece
                    else (255, 255, 255)
                )

                items.append(
                    (event.spin_type, spin_color, True)
                )


            # ====================
            # Line Clear
            # ====================

            if event.clear_type is not None:

                items.append(
                    (event.clear_type, (255, 255, 255), True)
                )


        # ====================
        # B2B (Persistent)
        # ====================

        if display_b2b > 0:

            items.append(
                (f"B2B ×{display_b2b}", (255, 220, 0), False)
            )


        # ====================
        # Combo
        # ====================

        if event.timer > 0 and event.combo > 0:

            items.append(
                (f"{event.combo} COMBO", (255, 255, 255), True)
            )


        if not items:
            return


        # ====================
        # Alpha Calculation
        # ====================

        alpha = min(
            255,
            int(
                255
                * min(
                    event.timer / game.CLEAR_EVENT_TIME,
                    1.0
                )
            )
        )


        for index, (text, color, fades) in enumerate(items):

            surface = self.stat_font.render(
                text,
                True,
                color
            )

            if fades:

                surface.set_alpha(
                    alpha
                )


            rect = surface.get_rect(
                right=right_align_x,
                y=y + index * 28
            )


            screen.blit(
                surface,
                rect
            )


    def get_clear_event_height(
        self,
        game
    ) -> int:
        """
        Returns the height required by the current clear event.
        """

        event = game.clear_event

        lines = 0

        display_b2b = max(
            game.back_to_back - 1,
            0
        )

        if event.timer > 0:

            if event.spin_type is not None:
                lines += 1

            if event.clear_type is not None:
                lines += 1

            if event.combo > 0:
                lines += 1

        if display_b2b > 0:
            lines += 1


        return lines * 28
