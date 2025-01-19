# backend/utils/code_quality.py

import subprocess


def run_flake8():
    """Run Flake8 to check code for PEP 8 compliance."""
    result = subprocess.run(["flake8", "backend/"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Flake8 Issues Found:")
        print(result.stdout)
    else:
        print("Flake8: No issues found.")


def run_black():
    """Run Black to check code for PEP 8 compliance."""
    result = subprocess.run(
        ["black", "--check", "backend/"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("reformatted")
        print(result.stdout)
    else:
        print("unchanged")


if __name__ == "__main__":
    run_flake8()
    run_black()
