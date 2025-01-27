import pytest
from backend.utils.code_quality import run_flake8, run_black


@pytest.mark.usefixtures("function_db_setup")
def test_run_flake8(capsys):
    """
    Ensures Flake8 is run and any issues are printed,
    causing a nonzero exit if violations exist.
    """
    with pytest.raises(SystemExit) as exc_info:
        run_flake8()

    captured = capsys.readouterr()
    # If Flake8 fails, it prints "Flake8 Issues Found:" and exits with returncode != 0
    assert "Flake8 Issues Found:" in captured.out or "Flake8: No issues found." in captured.out
    assert exc_info.value.code != 0 or "No issues found." in captured.out


@pytest.mark.usefixtures("function_db_setup")
def test_run_black(capsys):
    """
    Ensures Black is run and any issues are printed,
    causing a nonzero exit if formatting is incorrect.
    """
    with pytest.raises(SystemExit) as exc_info:
        run_black()

    captured = capsys.readouterr()
    # If Black fails, it prints "Black Issues Found:" and exits with returncode != 0
    assert "Black Issues Found:" in captured.out or "Black: No issues found." in captured.out
    assert exc_info.value.code != 0 or "No issues found." in captured.out
