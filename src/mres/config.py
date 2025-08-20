"""Basic configurations."""
# standard
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
TEST_DIR = ROOT_DIR / "tests"

if __name__ == "__main__":
    print(f"{ROOT_DIR=}")
    print(f"{TEST_DIR=}")
