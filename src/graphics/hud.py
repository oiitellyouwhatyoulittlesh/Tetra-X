"""
Tetra-X

File:
    hud.py

Purpose:
    Draws the game's HUD.
"""

import pygame

from constants import (
    BOARD_COLUMNS,
    BORDER,
    CELL_SIZE,
    GARBAGE_GREY,
)
from game.modes import GameMode
from game.pieces import (
    get_cells,
    get_colour,
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
    MINI_CELL_SIZE = 28
    HEADER_HEIGHT = 28


    def __init__(self) -> None:
        """
        Creates HUD font resources.
        """
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.stat_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.value_font = pygame.font.SysFont("Arial", 22)


    # ====================
    # Drawing
    # ====================

    def draw(
        self,
        screen,
        game,
        board_x: int,
        board_y: int,
        zen_topout: bool = False
    ) -> None:
        """
        Draws the main HUD overlay on screen.
        """
        board = game.get_board()
        board_width = BOARD_COLUMNS * CELL_SIZE

        hold_x = board_x - self.GAP - self.PANEL_WIDTH
        next_x = board_x + board_width + self.GAP

        self.draw_hold_panel(screen, board, hold_x, board_y, zen_topout)
        self.draw_next_panel(screen, board, next_x, board_y, zen_topout)

        if game.settings.display_controls:
            self.draw_controls(
                screen,
                game,
                next_x + self.PANEL_WIDTH + self.GAP,
                board_y
            )

        self.draw_game_stats(screen, game, board_x, board_y, board_width)


    # ====================
    # Panels
    # ====================

    def draw_hold_panel(
        self,
        screen,
        board,
        x: int,
        y: int,
        zen_topout: bool = False
    ) -> None:
        """
        Draws the hold piece panel.
        """
        points = [
            (x, y),
            (x + self.PANEL_WIDTH, y),
            (x + self.PANEL_WIDTH, y + self.HOLD_HEIGHT),
            (x + self.CORNER, y + self.HOLD_HEIGHT),
            (x, y + self.HOLD_HEIGHT - self.CORNER)
        ]

        pygame.draw.polygon(screen, BORDER, points, 2)
        pygame.draw.rect(screen, BORDER, (x, y, self.PANEL_WIDTH, self.HEADER_HEIGHT))

        label_surface = self.font.render("HOLD", True, (0, 0, 0))
        label_rect = label_surface.get_rect(
            left=x + 10,
            centery=y + self.HEADER_HEIGHT // 2
        )

        screen.blit(label_surface, label_rect)

        if board.held_piece is not None:
            content_center_y = int(
                y + self.HEADER_HEIGHT + (self.HOLD_HEIGHT - self.HEADER_HEIGHT) / 2
            )

            self.draw_mini_piece(
                screen,
                board.held_piece,
                x + self.PANEL_WIDTH // 2,
                content_center_y,
                GARBAGE_GREY if zen_topout or not board.can_hold else None,
                max_width=self.PANEL_WIDTH - 20,
                max_height=self.HOLD_HEIGHT - self.HEADER_HEIGHT - 10
            )


    def draw_next_panel(
        self,
        screen,
        board,
        x: int,
        y: int,
        zen_topout: bool = False
    ) -> None:
        """
        Draws the next piece preview panel with evenly distributed queue items.
        """
        points = [
            (x, y),
            (x + self.PANEL_WIDTH, y),
            (x + self.PANEL_WIDTH, y + self.NEXT_HEIGHT - self.CORNER),
            (x + self.PANEL_WIDTH - self.CORNER, y + self.NEXT_HEIGHT),
            (x, y + self.NEXT_HEIGHT)
        ]

        pygame.draw.polygon(screen, BORDER, points, 2)
        pygame.draw.rect(screen, BORDER, (x, y, self.PANEL_WIDTH, self.HEADER_HEIGHT))

        label_surface = self.font.render("NEXT", True, (0, 0, 0))
        label_rect = label_surface.get_rect(
            left=x + 10,
            centery=y + self.HEADER_HEIGHT // 2
        )

        screen.blit(label_surface, label_rect)

        preview = board.get_preview()
        preview_count = 5

        usable_y_start = y + self.HEADER_HEIGHT
        usable_height = self.NEXT_HEIGHT - self.HEADER_HEIGHT
        slot_height = usable_height / preview_count

        for index, piece in enumerate(preview[:preview_count]):
            center_x = x + self.PANEL_WIDTH // 2
            center_y = int(usable_y_start + (index + 0.5) * slot_height)

            self.draw_mini_piece(
                screen,
                piece,
                center_x,
                center_y,
                GARBAGE_GREY if zen_topout else None,
                max_width=self.PANEL_WIDTH - 20,
                max_height=int(slot_height - 10)
            )


    # ====================
    # Controls Display
    # ====================

    def draw_controls(self, screen, game, x: int, y: int) -> None:
        """
        Draws current active gameplay key bindings on screen.
        """
        y += CELL_SIZE

        self.draw_label(screen, "CONTROLS", x, y - 32)

        actions = [
            ("Move Left", "move_left"),
            ("Move Right", "move_right"),
            ("Soft Drop", "soft_drop"),
            ("Hard Drop", "hard_drop"),
            ("Rotate CW", "rotate_cw"),
            ("Rotate CCW", "rotate_ccw"),
            ("Rotate 180", "rotate_180"),
            ("Hold", "hold"),
            ("Pause", "pause"),
            ("Restart", "restart"),
        ]

        line_spacing = 30

        for index, (label_text, action_key) in enumerate(actions):
            key_name = game.settings.get_control_name(action_key)

            label_surface = self.stat_font.render(label_text, True, BORDER)
            value_surface = self.value_font.render(key_name, True, BORDER)

            current_y = y + index * line_spacing

            screen.blit(label_surface, (x, current_y))
            screen.blit(value_surface, (x + 150, current_y))


    # ====================
    # Mini Pieces Rendering
    # ====================

    def draw_mini_piece(
        self,
        screen,
        piece: str,
        center_x: int,
        center_y: int,
        override_colour=None,
        max_width: int | None = None,
        max_height: int | None = None
    ) -> None:
        """
        Draws a centered miniature piece preview scaled to fit its panel space cleanly.
        """
        cells = get_cells(piece, 0)
        colour = override_colour if override_colour is not None else get_colour(piece)

        min_x = min(x for x, _ in cells)
        max_x = max(x for x, _ in cells)
        min_y = min(y for _, y in cells)
        max_y = max(y for _, y in cells)

        cols = max_x - min_x + 1
        rows = max_y - min_y + 1

        cell_size = float(self.MINI_CELL_SIZE)

        if max_width and (cols * cell_size > max_width):
            cell_size = max_width / cols

        if max_height and (rows * cell_size > max_height):
            cell_size = min(cell_size, max_height / rows)

        piece_width = cols * cell_size
        piece_height = rows * cell_size

        start_x = center_x - piece_width / 2
        start_y = center_y - piece_height / 2

        for cell_x, cell_y in cells:
            x = start_x + (cell_x - min_x) * cell_size
            y = start_y + (cell_y - min_y) * cell_size

            rectangle = pygame.Rect(
                int(x),
                int(y),
                int(cell_size),
                int(cell_size)
            )

            pygame.draw.rect(screen, colour, rectangle.inflate(-2, -2))


    # ====================
    # Text Utilities
    # ====================

    def draw_label(self, screen, text: str, x: int, y: int) -> None:
        """
        Draws a generic HUD label.
        """
        surface = self.font.render(text, True, BORDER)
        screen.blit(surface, (x, y))


    # ====================
    # Game Stats Rendering
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
        Draws gameplay statistics based on the active game mode.
        """
        right_align_x = board_x - self.GAP
        bottom_y = screen.get_height() - 460

        label_colour = (255, 255, 255)
        value_colour = (255, 255, 255)

        if game.mode == GameMode.BLITZ:
            total_milliseconds = int(game.blitz_time * 1000)
            minutes = total_milliseconds // 60000
            seconds = (total_milliseconds // 1000) % 60
            milliseconds = total_milliseconds % 1000

            time_text = f"{minutes}:{seconds:02d}.{milliseconds:03d}"

            stats = [
                ("SCORE", f"{game.score:,}"),
                ("TIME", time_text),
                ("LEVEL", str(game.level)),
                ("LINES", f"{game.level_lines} / {game.level_line_goal}")
            ]

        elif game.mode == GameMode.FORTY_LINES:
            display_time = (
                game.completion_time
                if game.completed
                else game.game_time
            )

            total_milliseconds = int(display_time * 1000)
            minutes = total_milliseconds // 60000
            seconds = (total_milliseconds // 1000) % 60
            milliseconds = total_milliseconds % 1000

            time_text = f"{minutes}:{seconds:02d}.{milliseconds:03d}"

            inputs = game.inputs
            pieces = game.pieces_placed

            inputs_per_piece = inputs / pieces if pieces > 0 else 0.0
            pieces_per_second = pieces / display_time if display_time > 0 else 0.0

            stats = [
                ("LINES", f"{game.lines_cleared} / 40"),
                ("TIME", time_text),
                ("PIECES", f"{pieces}, {pieces_per_second:.2f}/S"),
                ("INPUTS", f"{inputs}, {inputs_per_piece:.2f}/P")
            ]

        else:
            inputs = game.inputs
            pieces = game.pieces_placed

            inputs_per_piece = inputs / pieces if pieces > 0 else 0.0
            pieces_per_second = pieces / game.game_time if game.game_time > 0 else 0.0

            total_milliseconds = int(game.game_time * 1000)
            minutes = total_milliseconds // 60000
            seconds = (total_milliseconds // 1000) % 60
            milliseconds = total_milliseconds % 1000

            time_text = f"{minutes}:{seconds:02d}.{milliseconds:03d}"

            stats = [
                ("INPUTS", f"{inputs}, {inputs_per_piece:.2f}/P"),
                ("PIECES", f"{pieces}, {pieces_per_second:.2f}/S"),
                ("LINES", str(game.lines_cleared)),
                ("TIME", time_text)
            ]

        hold_bottom = board_y + self.HOLD_HEIGHT
        stats_top = bottom_y
        middle_space = stats_top - hold_bottom

        event_height = self.get_clear_event_height(game)
        event_y = hold_bottom + middle_space // 2 - event_height // 2

        self.draw_clear_event(screen, game, right_align_x, event_y)

        line_height = 42
        y = bottom_y

        for label, value in stats:
            label_surface = self.stat_font.render(label, True, label_colour)
            value_surface = self.value_font.render(value, True, value_colour)

            label_rect = label_surface.get_rect(right=right_align_x, y=y)
            value_rect = value_surface.get_rect(right=right_align_x, y=y + 22)

            screen.blit(label_surface, label_rect)
            screen.blit(value_surface, value_rect)

            y += line_height + 22


    # ====================
    # Clear Event Announcements
    # ====================

    def draw_clear_event(
        self,
        screen,
        game,
        right_align_x: int,
        y: int
    ) -> None:
        """
        Draws temporary line clear announcements and active Back-to-Back status.
        """
        event = game.clear_event
        items = []

        display_b2b = max(game.back_to_back - 1, 0)

        if event.timer > 0:
            if event.spin_type is not None:
                spin_color = (
                    get_colour(event.spin_piece)
                    if event.spin_piece
                    else (255, 255, 255)
                )
                items.append((event.spin_type, spin_color, True))

            if event.clear_type is not None:
                items.append((event.clear_type, (255, 255, 255), True))

        if display_b2b > 0:
            items.append((f"B2B ×{display_b2b}", (255, 220, 0), False))

        if event.timer > 0 and event.combo > 0:
            items.append((f"{event.combo} COMBO", (255, 255, 255), True))

        if not items:
            return

        alpha = min(
            255,
            int(255 * min(event.timer / game.CLEAR_EVENT_TIME, 1.0))
        )

        for index, (text, color, fades) in enumerate(items):
            surface = self.stat_font.render(text, True, color)

            if fades:
                surface.set_alpha(alpha)

            rect = surface.get_rect(right=right_align_x, y=y + index * 28)
            screen.blit(surface, rect)


    def get_clear_event_height(self, game) -> int:
        """
        Returns total screen height required by the current active clear event text.
        """
        event = game.clear_event
        lines = 0

        display_b2b = max(game.back_to_back - 1, 0)

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
