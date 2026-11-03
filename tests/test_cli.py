from tests.conftest import HIDDEN
from veritiscan.cli import main


def test_cli_prints_findings(white_text_pdf, capsys):
    assert main([str(white_text_pdf)]) == 0
    assert capsys.readouterr().out.strip() == f"page 1\twhite_text\t{HIDDEN}"


def test_cli_clean_pdf_prints_nothing(clean_pdf, capsys):
    assert main([str(clean_pdf)]) == 0
    assert capsys.readouterr().out == ""


def test_cli_missing_file_exits_2(tmp_path):
    assert main([str(tmp_path / "missing.pdf")]) == 2


def test_cli_not_a_pdf_exits_2(tmp_path):
    bogus = tmp_path / "fake.pdf"
    bogus.write_text("not a pdf")
    assert main([str(bogus)]) == 2
