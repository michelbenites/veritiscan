import argparse
import sys
from pathlib import Path

from veritiscan.scanner import scan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="veritiscan", description="Detect hidden text in a PDF file."
    )
    parser.add_argument("pdf", type=Path, help="path to a PDF file")
    args = parser.parse_args(argv)

    if not args.pdf.is_file():
        print(f"error: file not found: {args.pdf}", file=sys.stderr)
        return 2
    try:
        findings = scan(args.pdf)
    except Exception as exc:  # pdfminer raises several error types for bad PDFs
        print(f"error: not a valid PDF: {args.pdf} ({exc})", file=sys.stderr)
        return 2

    for f in findings:
        print(f"page {f.page}\t{f.rule}\t{f.text}")
    return 0
