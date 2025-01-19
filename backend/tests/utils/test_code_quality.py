# backend/tests/utils/test_code_quality.py

from backend.utils.code_quality import run_flake8, run_black


def test_run_flake8(capsys):
    run_flake8()
    captured = capsys.readouterr()
    assert (
        "Flake8 Issues Found:" in captured.out
        or "Flake8: No issues found." in captured.out
    )


def test_run_black(capsys):
    run_black()
    captured = capsys.readouterr()
    assert "reformatted" in captured.out or "unchanged" in captured.out
