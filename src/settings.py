"""
Tetra-X

File:
    settings.py

Purpose:
    Loads and stores the game's settings.
"""

from dataclasses import dataclass

import pygame

from constants import (
    DEFAULT_SETTINGS,
    SETTINGS_FILE
)

from save.json_manager import (
    load_json,
    save_json
)


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


# Reverse lookup:
# pygame key -> settings.json name

REVERSE_KEY_MAP = {
    key: name
    for name, key in KEY_MAP.items()
}


# ====================
# Settings Classes
# ====================

@dataclass
class Controls:
    move_left: int
    move_right: int
    soft_drop: int
    hard_drop: int
    rotate_cw: int
    rotate_ccw: int
    rotate_180: int
    hold: int
    pause: int
    restart: int

    menu_up: int
    menu_down: int
    menu_confirm: int
    menu_back: int


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
    Stores all game settings.
    """

    def __init__(self) -> None:

        data = load_json(
            SETTINGS_FILE,
            DEFAULT_SETTINGS
        )

        self.controls = self._load_controls(
            data["controls"]
        )

        self.handling = self._load_handling(
            data["handling"]
        )

        self.video = Video(
            fullscreen=data["video"].get(
                "fullscreen",
                True
            )
        )


    # ====================
    # Loading
    # ====================

    def _load_controls(
        self,
        data: dict
    ) -> Controls:
        """
        Loads the control settings.
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


    def _load_handling(
        self,
        data: dict
    ) -> Handling:
        """
        Loads the handling settings.
        """

        sdf = data["sdf"]

        if sdf == "inf":

            sdf = float("inf")


        return Handling(
            das=max(
                1.0,
                min(
                    20.0,
                    float(data["das"])
                )
            ),

            arr=max(
                0.0,
                min(
                    5.0,
                    float(data["arr"])
                )
            ),

            dcd=max(
                0.0,
                min(
                    20.0,
                    float(data["dcd"])
                )
            ),

            sdf=sdf,

            prevent_hard_drop=data.get(
                "prevent_hard_drop",
                False
            ),

            cancel_das=data.get(
                "cancel_das",
                True
            ),

            prefer_soft_drop=data.get(
                "prefer_soft_drop",
                False
            )
        )


    # ====================
    # Control Settings
    # ====================

    def get_control(
        self,
        action: str
    ) -> int | None:
        """
        Returns the pygame key bound to an action.
        """

        return getattr(
            self.controls,
            action,
            None
        )


    def get_control_name(
        self,
        action: str
    ) -> str:
        """
        Returns the readable key name for an action.
        """

        key = self.get_control(
            action
        )

        if key is None:
            return "UNKNOWN"

        if key in REVERSE_KEY_MAP:
            return REVERSE_KEY_MAP[key]

        return pygame.key.name(key).upper()


    def set_control(
        self,
        action: str,
        key: int
    ) -> bool:
        """
        Changes the key bound to an action.

        Returns True if the action exists.
        """

        if not hasattr(
            self.controls,
            action
        ):
            return False


        setattr(
            self.controls,
            action,
            key
        )


        return True


    # ====================
    # Reset
    # ====================

    def reset(self) -> None:
        """
        Restores all settings to their default values
        and saves them to the settings file.
        """

        data = DEFAULT_SETTINGS


        self.controls = self._load_controls(
            data["controls"]
        )

        self.handling = self._load_handling(
            data["handling"]
        )

        self.video = Video(
            fullscreen=data["video"].get(
                "fullscreen",
                True
            )
        )

        self.save()


    # ====================
    # Saving
    # ====================

    def save(self) -> None:
        """
        Saves the current settings to JSON.
        """

        controls = {}

        for action in (
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
        ):

            key = self.get_control(
                action
            )

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

            "prevent_hard_drop":
                self.handling.prevent_hard_drop,

            "cancel_das":
                self.handling.cancel_das,

            "prefer_soft_drop":
                self.handling.prefer_soft_drop
        }


        video = {
            "fullscreen":
                self.video.fullscreen
        }


        data = {
            "video": video,
            "controls": controls,
            "handling": handling
        }


        save_json(
            SETTINGS_FILE,
            data
        )
