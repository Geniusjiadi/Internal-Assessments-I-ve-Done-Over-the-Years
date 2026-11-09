from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PHASES = [
    ("Phase 1 - calculations and validation", [
        "tests.test_sleep_calculator",
        "tests.test_validation",
    ]),
    ("Phase 2 - database persistence", [
        "tests.test_database",
    ]),
    ("Phase 3 - analytics", [
        "tests.test_analytics",
    ]),
    ("Phase 4 - correlation engine", [
        "tests.test_correlation",
    ]),
    ("Phase 5 - pattern and recommendation engines", [
        "tests.test_patterns",
        "tests.test_recommendations",
    ]),
    ("Phase 6 - goals", [
        "tests.test_goals",
    ]),
]


def run_modules(title, modules):
    print(f"\n=== {title} ===")
    cmd = [sys.executable, "-m", "unittest", "-v", *modules]
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_api_tests():
    print("\n=== Phase 7 - Flask API integration ===")
    try:
        import flask  # noqa
    except ImportError:
        print("SKIPPED: Flask is not installed. Run `pip install -r requirements.txt` first.")
        return
    result = subprocess.run([sys.executable, "-m", "unittest", "-v", "tests.test_api"], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", action="store_true", help="Also run Flask API integration tests.")
    args = parser.parse_args()

    for title, modules in PHASES:
        run_modules(title, modules)

    if args.api:
        run_api_tests()

    print("\nAll requested progressive test phases passed.")


if __name__ == "__main__":
    main()
