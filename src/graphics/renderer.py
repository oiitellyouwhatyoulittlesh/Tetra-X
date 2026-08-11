"""
Tetra-X

File:
    renderer.py

Purpose:
    Handles drawing the game graphics.

"""

import pygame

from constants import (
    CELL_SIZE,
    BOARD_COLUMNS,
    VISIBLE_ROWS,
    BACKGROUND,
    GRID
)

from graphics.hud import HUD


class Renderer:
    """
    Handles rendering the game.
    """


    def __init__(self) -> None:

        pygame.init()


        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )


        pygame.display.set_caption(
            "Tetra-X"
        )


        self.screen_width = (
            self.screen.get_width()
        )

        self.screen_height = (
            self.screen.get_height()
        )


        self.board_x = (
            self.screen_width
            - BOARD_COLUMNS * CELL_SIZE
        ) // 2


        self.board_y = (
            self.screen_height
            - VISIBLE_ROWS * CELL_SIZE
        ) // 2


        self.hud = HUD()


        self.menu_title_font = pygame.font.Font(
            None,
            72
        )

        self.menu_option_font = pygame.font.Font(
            None,
            42
        )


    # ====================
    # Drawing
    # ====================

    def clear(self) -> None:
        """
        Clears the screen.
        """

        self.screen.fill(
            BACKGROUND
        )
    

    def draw_screen(
        self,
        screen
    ) -> None:
        """
        Draws a menu or other screen.
        """

        screen.draw(
            self
        )


    def draw_menu(
        self,
        title: str,
        options: list[str],
        selected: int
    ) -> None:
        """
        Draws a menu screen.
        """

        self.clear()


        # ====================
        # Title
        # ====================

        title_surface = self.menu_title_font.render(
            title,
            True,
            (255, 255, 255)
        )

        title_rectangle = title_surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 3
            )
        )

        self.screen.blit(
            title_surface,
            title_rectangle
        )


        # ====================
        # Options
        # ====================

        option_spacing = 70

        start_y = (
            self.screen_height // 2
        )


        for index, option in enumerate(options):

            if index == selected:

                text = (
                    "> "
                    + option
                )

            else:

                text = option


            option_surface = self.menu_option_font.render(
                text,
                True,
                (255, 255, 255)
            )


            option_rectangle = option_surface.get_rect(
                center=(
                    self.screen_width // 2,
                    start_y
                    + index * option_spacing
                )
            )


            self.screen.blit(
                option_surface,
                option_rectangle
            )


    def draw_board(self, game) -> None:
        """
        Draws the board and pieces.
        """

        board = game.get_board()

        OFFSET = (
            len(board.grid)
            - VISIBLE_ROWS
        )


        # ====================
        # Visible Grid + Locked Blocks
        # ====================

        for screen_y in range(
            VISIBLE_ROWS
        ):

            board_y = (
                screen_y
                + OFFSET
            )


            for x in range(
                BOARD_COLUMNS
            ):

                self.draw_cell(
                    x,
                    screen_y,
                    board.grid[board_y][x]
                )


        # ====================
        # Hidden Locked Blocks
        # ====================

        for board_y in range(
            OFFSET
        ):

            for x in range(
                BOARD_COLUMNS
            ):

                cell = board.grid[board_y][x]

                if cell:

                    screen_y = (
                        board_y
                        - OFFSET
                    )

                    self.draw_cell(
                        x,
                        screen_y,
                        cell
                    )


        # ====================
        # Ghost Piece
        # ====================

        ghost = board.get_ghost_piece()

        if ghost:

            ghost_colour = tuple(
                value // 3
                for value in ghost.colour
            )

            self.draw_piece(
                ghost,
                OFFSET,
                ghost_colour
            )


        # ====================
        # Active Piece
        # ====================

        if board.current_piece:

            self.draw_piece(
                board.current_piece,
                OFFSET,
                board.current_piece.colour
            )


        self.hud.draw(
            self.screen,
            game,
            self.board_x,
            self.board_y
        )


        # ====================
        # Countdown / Announcements
        # ====================

        if game.countdown_active:

            self.draw_countdown(
                game.countdown
            )

        elif game.clear_event.perfect_clear:

            self.draw_perfect_clear(
                game
            )


    def draw_countdown(
        self,
        countdown: float
    ) -> None:
        """
        Draws the game start countdown.
        """

        number = int(countdown) + 1

        font = pygame.font.Font(
            None,
            96
        )

        surface = font.render(
            str(number),
            True,
            (255, 220, 0)
        )

        rectangle = surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2
            )
        )

        self.screen.blit(
            surface,
            rectangle
        )


    def draw_perfect_clear(
        self,
        game
    ) -> None:
        """
        Draws the Perfect Clear announcement
        in the centre of the screen with a smooth fade.
        """

        font = pygame.font.Font(
            None,
            72
        )

        alpha = min(
            255,
            int(
                255
                * min(
                    game.clear_event.timer
                    / game.CLEAR_EVENT_TIME,
                    1.0
                )
            )
        )

        surface = font.render(
            "PERFECT CLEAR",
            True,
            (255, 215, 0)
        )

        surface.set_alpha(
            alpha
        )

        rectangle = surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2
            )
        )

        self.screen.blit(
            surface,
            rectangle
        )


    def draw_piece(
        self,
        piece,
        offset,
        colour
    ) -> None:
        """
        Draws a piece anywhere on the backend board.
        """

        for x, y in piece.get_cells():

            screen_y = (
                y
                - offset
            )

            self.draw_cell(
                x,
                screen_y,
                colour
            )


    def draw_cell(
        self,
        x: int,
        y: int,
        colour
    ) -> None:
        """
        Draws a single board cell.
        """

        rectangle = pygame.Rect(
            self.board_x + x * CELL_SIZE,
            self.board_y + y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(
            self.screen,
            GRID,
            rectangle,
            1
        )

        if colour:

            pygame.draw.rect(
                self.screen,
                colour,
                rectangle.inflate(
                    -2,
                    -2
                )
            )


    def update(self) -> None:
        """
        Updates the display.
        """

        pygame.display.flip()
