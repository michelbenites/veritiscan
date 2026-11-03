from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    """A hidden-text finding: a whole text span flagged by one rule."""

    file: str
    page: int  # 1-based
    rule: str
    text: str
    bbox: tuple[float, float, float, float]  # x0, top, x1, bottom
