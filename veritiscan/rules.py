"""Detection rules. Each rule takes a Span and returns True if it is suspicious."""

from collections.abc import Callable
from dataclasses import dataclass

TINY_FONT_THRESHOLD = 2.0  # points; spans with a smaller size are flagged


@dataclass(frozen=True)
class Span:
    """Consecutive characters on a page sharing the same style."""

    text: str
    size: float
    color: tuple[float, ...]  # non-stroking (fill) color components
    bbox: tuple[float, float, float, float]


def white_text(span: Span) -> bool:
    """Fill color is white: gray 1, RGB (1,1,1) or CMYK (0,0,0,0)."""
    c = span.color
    if len(c) in (1, 3):
        return all(v == 1 for v in c)
    if len(c) == 4:
        return all(v == 0 for v in c)
    return False


def tiny_font(span: Span) -> bool:
    """Font size is below TINY_FONT_THRESHOLD points."""
    return span.size < TINY_FONT_THRESHOLD


RULES: dict[str, Callable[[Span], bool]] = {
    "white_text": white_text,
    "tiny_font": tiny_font,
}
