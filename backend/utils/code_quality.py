# File: backend/utils/code_quality.py

import subprocess
import sys


def run_flake8():
    """Run Flake8 to check code for PEP 8 compliance."""
    try:
        result = subprocess.run(
            ["flake8", "backend/"],
            capture_output=True,
            text=True,
            check=False,  # Explicitly define check
        )
        if result.returncode != 0:
            print("Flake8 Issues Found:")
            print(result.stdout)
            sys.exit(result.returncode)
        else:
            print("Flake8: No issues found.")
    except FileNotFoundError:
        print("Flake8 is not installed. Please install it using `pip install flake8`.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Flake8: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred while running Flake8: {e}")
        sys.exit(1)


def run_black():
    """Run Black to check code for PEP 8 compliance."""
    try:
        result = subprocess.run(
            ["black", "--check", "backend/"],
            capture_output=True,
            text=True,
            check=False,  # Explicitly define check
        )
        if result.returncode != 0:
            print("Black Issues Found:")
            print(result.stdout)
            sys.exit(result.returncode)
        else:
            print("Black: No issues found.")
    except FileNotFoundError:
        print("Black is not installed. Please install it using `pip install black`.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Black: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred while running Black: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_flake8()
    run_black()
