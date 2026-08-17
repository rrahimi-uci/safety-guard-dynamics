"""Regression tests for the FAccT matched-false-alarm reconstruction."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


_MODULE = Path(__file__).resolve().parents[1] / "papers" / "unified-report" / "matched_fpr.py"
_SPEC = spec_from_file_location("facct_matched_fpr", _MODULE)
assert _SPEC and _SPEC.loader
_MATCHED_FPR = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MATCHED_FPR)


def test_threshold_is_conservative_when_all_negative_scores_are_tied():
    """An indivisible tied block cannot be partly admitted to hit a five-percent budget."""

    threshold = _MATCHED_FPR.threshold_at_most_fpr([1.0] * 20, 0.05)
    assert threshold == float("inf")


def test_threshold_keeps_the_largest_feasible_tied_block_outside_the_alarm_set():
    """The selected threshold maximizes admissions while preserving the empirical budget."""

    scores = [3.0, 3.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    threshold = _MATCHED_FPR.threshold_at_most_fpr(scores, 0.25)
    assert threshold == 3.0
    assert sum(score >= threshold for score in scores) / len(scores) == pytest.approx(0.2)
