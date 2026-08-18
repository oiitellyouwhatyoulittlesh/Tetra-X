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
# Special Mechanics Scores
# ====================

ALL_CLEAR_SCORE = 3500
HARD_DROP_SCORE = 2
SOFT_DROP_SCORE = 1


# ====================
# Line Clear Score Calculation
# ====================

def get_line_clear_score(cleared: int, level: int) -> int:
    """
    Returns the score awarded for clearing lines based on current level.
    """
    base_score = LINE_CLEAR_SCORES.get(cleared, 0)
    return base_score * level


# ====================
# T-Spin Score Calculation
# ====================

def get_t_spin_score(cleared: int, level: int, mini: bool = False) -> int:
    """
    Returns the score awarded for a T-Spin or Mini Spin.
    """
    spin_type = "mini" if mini else "normal"
    scores = T_SPIN_SCORES.get(spin_type, {})

    return scores.get(cleared, 0) * level


# ====================
# All Clear Score Calculation
# ====================

def get_all_clear_score(level: int) -> int:
    """
    Returns the score awarded for an All Clear board state.
    """
    return ALL_CLEAR_SCORE * level


# ====================
# Drop Score Calculations
# ====================

def get_hard_drop_score(cells: int) -> int:
    """
    Returns the score awarded for hard dropping a piece across distance.
    """
    return cells * HARD_DROP_SCORE


def get_soft_drop_score(cells: int) -> int:
    """
    Returns the score awarded for soft dropping a piece across distance.
    """
    return cells * SOFT_DROP_SCORE


# ====================
# Back-to-Back Logic & Bonus
# ====================

def is_difficult_clear(
    cleared: int,
    spin_type: str | None = None,
    all_clear: bool = False
) -> bool:
    """
    Returns True if the line clear qualifies for a Back-to-Back streak.
    """
    if all_clear:
        return True

    if spin_type is not None and cleared > 0:
        return True

    return cleared >= 4


def apply_back_to_back(score: int) -> int:
    """
    Applies the Back-to-Back 1.5x score multiplier.
    """
    return int(score * 1.5)


# ====================
# Combo Bonus Calculation
# ====================

def get_combo_score(combo: int, level: int) -> int:
    """
    Returns the additional combo streak score bonus.
    """
    if combo <= 0:
        return 0

    return combo * 50 * level
