# veritiscan

A small CLI that detects hidden text in PDF files: text a human cannot see but an
AI text extractor still reads.

## Who is it for
People who use AI to read documents (for example law offices) and want to check a PDF before the AI reads it.

## Built with
Python (tested on 3.11 and 3.12) and pdfplumber (MIT). The tests use pytest and reportlab.

## Rules

- `white_text`: fill color is white (gray 1, RGB 1,1,1 or CMYK 0,0,0,0).
- `tiny_font`: font size below 2 pt (`TINY_FONT_THRESHOLD` in `veritiscan/rules.py`).

Findings are reported per text span (consecutive characters with the same font,
size and color), not per character.

## Usage

    pip install -r requirements.txt
    python -m veritiscan file.pdf

Output is one line per finding: `page N<TAB>rule<TAB>text`.
Exit code is 0 on success and 2 if the file does not exist or is not a PDF.

## Development

    pip install -r requirements-dev.txt
    python -m pytest -q

Tests build their own PDFs with reportlab. The samples/ folder has small files for manual runs of the CLI.
