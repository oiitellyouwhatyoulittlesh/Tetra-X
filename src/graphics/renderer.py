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



    def draw_board(self, board) -> None:
        """
        Draws the board and pieces.
        """
    
    
        # Backend:
        # 0-39
        #
        # Visible:
        # 20-39
        #
        # Screen:
        # 0-19
    
    
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
            board,
            self.board_x,
            self.board_y
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
