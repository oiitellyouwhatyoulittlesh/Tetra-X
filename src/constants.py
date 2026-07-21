"""
Tetra-X

File:
    constants.py

Purpose:
    Stores constant values used throughout the game.

"""

# ====================
# Game
# ====================

TITLE = "Tetra-X"
VERSION = "1.0.0"

FPS = 60

# ====================
# Screen
# ====================

CELL_SIZE = 32

VISIBLE_ROWS = 20
BOARD_ROWS = 40
BOARD_COLUMNS = 10

# ====================
# Timing
# ====================

# In frames
LOCK_DELAY = 30
LINE_CLEAR_DELAY = 20

# ====================
# Piece Colours
# ====================

PIECE_I = (0, 255, 255)
PIECE_O = (255, 255, 0)
PIECE_T = (160, 0, 240)
PIECE_S = (0, 255, 0)
PIECE_Z = (255, 0, 0)
PIECE_J = (0, 0, 255)
PIECE_L = (255, 140, 0)

# ====================
# UI Colours
# ====================

BACKGROUND = (20, 20, 20)
GRID = (45, 45, 45)
TEXT = (255, 255, 255)
SHADOW = (0, 0, 0)

# ====================
# File Paths
# ====================

SETTINGS_FILE = "settings.json"
STATISTICS_FILE = "data/statistics.json"

REPLAY_FOLDER = "data/replays"

FONT_FOLDER = "assets/fonts"
SKIN_FOLDER = "assets/skins"
SOUND_FOLDER = "assets/sounds"

# ====================
# Default Settings
# ====================

DEFAULT_SETTINGS = {
    "video": {
        "fullscreen": True
    },

    "controls": {
        "move_left": "LEFT",
        "move_right": "RIGHT",
        "soft_drop": "DOWN",
        "hard_drop": "SPACE",

        "rotate_cw": "UP",
        "rotate_ccw": "z",
        "rotate_180": "x",

        "hold": "c",

        "pause": "ESCAPE",
        "restart": "r"
    },

    "handling": {
        "das": 10.0,
        "arr": 2.0,
        "dcd": 0.0,
        "sdf": 20
    }
}
