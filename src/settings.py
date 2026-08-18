"""
Tetra-X

File:
    settings.py

Purpose:
    Loads, manages, and stores all user settings and control key mappings.
"""

from dataclasses import dataclass

import pygame

from constants import DEFAULT_SETTINGS, SETTINGS_FILE
from save.json_manager import load_json, save_json

# ====================
# Key Map
# ====================

KEY_MAP = {
    # Directional / Navigation
    "LEFT": pygame.K_LEFT,
    "RIGHT": pygame.K_RIGHT,
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "SPACE": pygame.K_SPACE,
    "ESCAPE": pygame.K_ESCAPE,
    "RETURN": pygame.K_RETURN,
    "TAB": pygame.K_TAB,
    "BACKSPACE": pygame.K_BACKSPACE,
    "DELETE": pygame.K_DELETE,
    "INSERT": pygame.K_INSERT,
    "HOME": pygame.K_HOME,
    "END": pygame.K_END,
    "PAGEUP": pygame.K_PAGEUP,
    "PAGEDOWN": pygame.K_PAGEDOWN,

    # Punctuation & Symbols
    ";": pygame.K_SEMICOLON,
    "'": pygame.K_QUOTE,
    ",": pygame.K_COMMA,
    ".": pygame.K_PERIOD,
    "/": pygame.K_SLASH,
    "\\": pygame.K_BACKSLASH,
    "[": pygame.K_LEFTBRACKET,
    "]": pygame.K_RIGHTBRACKET,
    "`": pygame.K_BACKQUOTE,
    "-": pygame.K_MINUS,
    "=": pygame.K_EQUALS,

    # Number Row
    "0": pygame.K_0,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,

    # Modifiers
    "LSHIFT": pygame.K_LSHIFT,
    "RSHIFT": pygame.K_RSHIFT,
    "LCTRL": pygame.K_LCTRL,
    "RCTRL": pygame.K_RCTRL,
    "LALT": pygame.K_LALT,
    "RALT": pygame.K_RALT,
    "CAPSLOCK": pygame.K_CAPSLOCK,

    # Function Keys
    "F1": pygame.K_F1,
    "F2": pygame.K_F2,
    "F3": pygame.K_F3,
    "F4": pygame.K_F4,
    "F5": pygame.K_F5,
    "F6": pygame.K_F6,
    "F7": pygame.K_F7,
    "F8": pygame.K_F8,
    "F9": pygame.K_F9,
    "F10": pygame.K_F10,
    "F11": pygame.K_F11,
    "F12": pygame.K_F12,

    # Alphabet
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z
}

# Reverse lookup: Pygame key integer -> JSON key string
REVERSE_KEY_MAP = {key: name for name, key in KEY_MAP.items()}


# ====================
# Settings Classes
# ====================

@dataclass
class Controls:
    move_left: int | None
    move_right: int | None
    soft_drop: int | None
    hard_drop: int | None
    rotate_cw: int | None
    rotate_ccw: int | None
    rotate_180: int | None
    hold: int | None
    pause: int | None
    restart: int | None

    menu_up: int | None
    menu_down: int | None
    menu_confirm: int | None
    menu_back: int | None


@dataclass
class Handling:
    das: float
    arr: float
    dcd: float
    sdf: float

    prevent_hard_drop: bool
    cancel_das: bool
    prefer_soft_drop: bool


@dataclass
class Video:
    fullscreen: bool


class Settings:
    """
    Stores and manages all active game configurations.
    """

    def __init__(self) -> None:
        data = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)

        self.controls = self._load_controls(data["controls"])
        self.handling = self._load_handling(data["handling"])
        self.video = Video(fullscreen=data["video"].get("fullscreen", True))
        self.display_controls = data.get("display_controls", True)


    # ====================
    # Loading Utilities
    # ====================

    def _load_controls(self, data: dict) -> Controls:
        """
        Parses control settings dictionary into a Controls instance.
        """
        return Controls(
            move_left=KEY_MAP[data["move_left"]],
            move_right=KEY_MAP[data["move_right"]],
            soft_drop=KEY_MAP[data["soft_drop"]],
            hard_drop=KEY_MAP[data["hard_drop"]],
            rotate_cw=KEY_MAP[data["rotate_cw"]],
            rotate_ccw=KEY_MAP[data["rotate_ccw"]],
            rotate_180=KEY_MAP[data["rotate_180"]],
            hold=KEY_MAP[data["hold"]],
            pause=KEY_MAP[data["pause"]],
            restart=KEY_MAP[data["restart"]],

            menu_up=KEY_MAP[data["menu_up"]],
            menu_down=KEY_MAP[data["menu_down"]],
            menu_confirm=KEY_MAP[data["menu_confirm"]],
            menu_back=KEY_MAP[data["menu_back"]]
        )


    def _load_handling(self, data: dict) -> Handling:
        """
        Parses handling settings dictionary into a Handling instance.
        """
        sdf = data["sdf"]
        if sdf == "inf":
            sdf = float("inf")

        return Handling(
            das=max(1.0, min(20.0, float(data["das"]))),
            arr=max(0.0, min(5.0, float(data["arr"]))),
            dcd=max(0.0, min(20.0, float(data["dcd"]))),
            sdf=sdf,
            prevent_hard_drop=data.get("prevent_hard_drop", False),
            cancel_das=data.get("cancel_das", True),
            prefer_soft_drop=data.get("prefer_soft_drop", False)
        )


    # ====================
    # Control Management
    # ====================

    def get_control(self, action: str) -> int | None:
        """
        Returns the Pygame key constant bound to the specified action string.
        """
        return getattr(self.controls, action, None)


    def get_control_name(self, action: str) -> str:
        """
        Returns a readable key display name for a specific control action.
        """
        key = self.get_control(action)

        if key is None:
            return "UNKNOWN"

        if key in REVERSE_KEY_MAP:
            return REVERSE_KEY_MAP[key]

        return pygame.key.name(key).upper()


    def set_control(self, action: str, key: int | None) -> bool:
        """
        Binds a Pygame key integer to a given control action.
        """
        if not hasattr(self.controls, action):
            return False

        setattr(self.controls, action, key)
        return True


    # ====================
    # Reset & Save
    # ====================

    def reset(self) -> None:
        """
        Restores default configuration values and updates saved file.
        """
        data = DEFAULT_SETTINGS

        self.controls = self._load_controls(data["controls"])
        self.handling = self._load_handling(data["handling"])
        self.video = Video(fullscreen=data["video"].get("fullscreen", True))
        self.display_controls = data.get("display_controls", True)

        self.save()


    def save(self) -> None:
        """
        Serializes current settings state to JSON file.
        """
        controls = {}
        action_keys = (
            "move_left",
            "move_right",
            "soft_drop",
            "hard_drop",
            "rotate_cw",
            "rotate_ccw",
            "rotate_180",
            "hold",
            "pause",
            "restart",
            "menu_up",
            "menu_down",
            "menu_confirm",
            "menu_back"
        )

        for action in action_keys:
            key = self.get_control(action)
            if key is None:
                continue

            if key in REVERSE_KEY_MAP:
                controls[action] = REVERSE_KEY_MAP[key]
            else:
                controls[action] = pygame.key.name(key).upper()

        handling = {
            "das": self.handling.das,
            "arr": self.handling.arr,
            "dcd": self.handling.dcd,
            "sdf": (
                "inf"
                if self.handling.sdf == float("inf")
                else self.handling.sdf
            ),
            "prevent_hard_drop": self.handling.prevent_hard_drop,
            "cancel_das": self.handling.cancel_das,
            "prefer_soft_drop": self.handling.prefer_soft_drop
        }

        video = {
            "fullscreen": self.video.fullscreen
        }

        data = {
            "video": video,
            "controls": controls,
            "handling": handling,
            "display_controls": self.display_controls
        }

        save_json(SETTINGS_FILE, data)
