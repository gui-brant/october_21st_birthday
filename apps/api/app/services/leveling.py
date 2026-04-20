from dataclasses import dataclass


def hours_required_for_level(level: int) -> float:
    if level <= 0:
        raise ValueError("level must be >= 1")
    if level <= 7:
        return 1.0
    if level <= 14:
        return 2.0
    if level <= 21:
        return 3.0
    if level <= 28:
        return 4.0
    if level <= 756:
        ratio = (level - 28) / (756 - 28)
        return 4.0 + (4.0 * ratio)
    if level <= 1848:
        ratio = (level - 756) / (1848 - 756)
        return 8.0 + (8.0 * ratio)
    return 16.0


def exp_required_for_level(level: int) -> float:
    return 100.0 * hours_required_for_level(level)


@dataclass
class LevelProgress:
    level_before: int
    level_after: int
    exp_after: float


def apply_exp(current_level: int, current_exp: float, gained_exp: float) -> LevelProgress:
    level = current_level
    exp = current_exp + gained_exp
    while exp >= exp_required_for_level(level):
        exp -= exp_required_for_level(level)
        level += 1
    return LevelProgress(level_before=current_level, level_after=level, exp_after=exp)
