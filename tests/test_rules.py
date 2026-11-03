from tests.conftest import HIDDEN
from veritiscan.rules import TINY_FONT_THRESHOLD, Span, tiny_font, white_text
from veritiscan.scanner import scan

BBOX = (0, 0, 1, 1)


def test_clean_pdf_has_no_findings(clean_pdf):
    assert scan(clean_pdf) == []


def test_white_text_finding(white_text_pdf):
    findings = scan(white_text_pdf)
    assert len(findings) == 1
    assert findings[0].rule == "white_text"
    assert findings[0].text == HIDDEN
    assert findings[0].page == 1


def test_cmyk_white_text(cmyk_white_pdf):
    assert [f.rule for f in scan(cmyk_white_pdf)] == ["white_text"]


def test_tiny_font_finding(tiny_font_pdf):
    findings = scan(tiny_font_pdf)
    assert len(findings) == 1
    assert findings[0].rule == "tiny_font"
    assert findings[0].text == HIDDEN


def test_hidden_text_on_second_page_only(two_page_pdf):
    findings = scan(two_page_pdf)
    assert [(f.page, f.text) for f in findings] == [(2, HIDDEN)]


def test_white_color_variants():
    assert white_text(Span("x", 12, (1,), BBOX))
    assert white_text(Span("x", 12, (1, 1, 1), BBOX))
    assert white_text(Span("x", 12, (0, 0, 0, 0), BBOX))
    assert not white_text(Span("x", 12, (0,), BBOX))
    assert not white_text(Span("x", 12, (), BBOX))


def test_tiny_font_threshold():
    assert tiny_font(Span("x", TINY_FONT_THRESHOLD - 0.1, (0,), BBOX))
    assert not tiny_font(Span("x", TINY_FONT_THRESHOLD, (0,), BBOX))
