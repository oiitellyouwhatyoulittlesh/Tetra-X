"""
Tetra-X

File:
    scoring.py

Purpose:
    Handles game scoring calculations.
"""


# ====================
# Line Clear Scores
# ====================

LINE_CLEAR_SCORES = {
    1: 100,
    2: 300,
    3: 500,
    4: 800
}


# ====================
# T-Spin Scores
# ====================

T_SPIN_SCORES = {
    "mini": {
        0: 100,
        1: 200,
        2: 400,
        3: 800,
        4: 1600
    },

    "normal": {
        0: 400,
        1: 800,
        2: 1200,
        3: 1600,
        4: 2600
    }
}


# ====================
# Perfect Clear
# ====================

PERFECT_CLEAR_SCORE = 3500


# ====================
# Drop Scores
# ====================

HARD_DROP_SCORE = 2
SOFT_DROP_SCORE = 1


# ====================
# Line Clear
# ====================

def get_line_clear_score(
    cleared: int,
    level: int
) -> int:
    """
    Returns the score awarded for clearing lines.
    """

    base_score = LINE_CLEAR_SCORES.get(
        cleared,
        0
    )

    return base_score * level


# ====================
# T-Spin
# ====================

def get_t_spin_score(
    cleared: int,
    level: int,
    mini: bool = False
) -> int:
    """
    Returns the score awarded for a T-spin or Mini Spin.
    """

    spin_type = (
        "mini"
        if mini
        else "normal"
    )

    scores = T_SPIN_SCORES.get(
        spin_type,
        {}
    )

    return (
        scores.get(
            cleared,
            0
        )
        * level
    )


# ====================
# Perfect Clear
# ====================

def get_perfect_clear_score(
    level: int
) -> int:
    """
    Returns the score awarded for a
    Perfect Clear.
    """

    return PERFECT_CLEAR_SCORE * level


# ====================
# Drop Score
# ====================

def get_hard_drop_score(
    cells: int
) -> int:
    """
    Returns the score awarded for
    hard dropping a piece.
    """

    return (
        cells
        * HARD_DROP_SCORE
    )


def get_soft_drop_score(
    cells: int
) -> int:
    """
    Returns the score awarded for
    soft dropping a piece.
    """

    return (
        cells
        * SOFT_DROP_SCORE
    )


# ====================
# Back-to-Back
# ====================

def is_difficult_clear(
    cleared: int,
    spin_type: str | None = None,
    perfect_clear: bool = False
) -> bool:
    """
    Returns True if the clear qualifies for Back-to-Back.
    """

    if perfect_clear:
        return True

    if spin_type is not None and cleared > 0:
        return True

    return cleared >= 4


# ====================
# Back-to-Back Bonus
# ====================

def apply_back_to_back(
    score: int
) -> int:
    """
    Applies the Back-to-Back 1.5x bonus.
    """

    return int(
        score * 1.5
    )


# ====================
# Combo Bonus
# ====================

def get_combo_score(
    combo: int,
    level: int
) -> int:
    """
    Returns the combo bonus.

    Combo 0 gives no bonus.
    Combo 1 gives 50 points.
    Combo 2 gives 100 points.
    """

    if combo <= 0:
        return 0

    return (
        combo
        * 50
        * level
    )
