# ============================================================
# tests/test_storytelling_case.py
# ============================================================
# WHY: Smoke test the example module to illustrate the role
# of tests in professional project workflows.
#
# Run:
#   uv run python -m pytest

from bizintel import storytelling_case


def test_storytelling_case_has_main() -> None:
    """Verify the example module exposes a main function."""
    assert callable(storytelling_case.main)
