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


    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        screen,
        board,
        board_x: int,
        board_y: int
    ) -> None:
        """
        Draws the HUD.
        """

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
        Draws a miniature tetromino centred at a position.
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
