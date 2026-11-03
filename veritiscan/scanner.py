from collections.abc import Iterator
from pathlib import Path

import pdfplumber

from veritiscan.models import Finding
from veritiscan.rules import RULES, Span


def _color(char: dict) -> tuple[float, ...]:
    """Normalize pdfplumber's fill color to a tuple of floats."""
    color = char.get("non_stroking_color")
    if color is None:
        return ()  # default fill (black); matches no rule
    if isinstance(color, (int, float)):
        return (float(color),)
    return tuple(float(v) for v in color if isinstance(v, (int, float)))


def _spans(chars: list[dict]) -> Iterator[Span]:
    """Group consecutive chars with the same font, size and color into spans."""
    group: list[dict] = []
    key = None
    for ch in chars:
        k = (ch["fontname"], round(ch["size"], 2), _color(ch))
        if group and k != key:
            yield _make_span(group)
            group = []
        group.append(ch)
        key = k
    if group:
        yield _make_span(group)


def _make_span(group: list[dict]) -> Span:
    return Span(
        text="".join(c["text"] for c in group),
        size=group[0]["size"],
        color=_color(group[0]),
        bbox=(
            min(c["x0"] for c in group),
            min(c["top"] for c in group),
            max(c["x1"] for c in group),
            max(c["bottom"] for c in group),
        ),
    )


def scan(path: str | Path) -> list[Finding]:
    """Scan a PDF and return one Finding per (span, rule) match."""
    findings: list[Finding] = []
    with pdfplumber.open(path) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            for span in _spans(page.chars):
                if not span.text.strip():
                    continue  # whitespace-only spans carry no content
                for name, rule in RULES.items():
                    if rule(span):
                        findings.append(
                            Finding(str(path), number, name, span.text.strip(), span.bbox)
                        )
    return findings
