"""
test_intrinsic_purity.py - Verification of @b-only enforcement in intrinsic calibration

This test ensures strict @b-only enforcement:
- NO keys matching @chain, @q, @d, @p, @C, @u, @m, final_score, layer_scores
- ONLY keys: intrinsic_score, b_theory, b_impl, b_deploy, calibration_status, layer, last_updated
- Coverage >= 80% (computed methods / total methods)
- At least 30 executors with status='computed'
"""
import json
from pathlib import Path

import pytest


def test_intrinsic_calibration_exists():
    """Verify intrinsic_calibration.json exists."""
    cal_path = Path("config/intrinsic_calibration.json")
    assert cal_path.exists(), "config/intrinsic_calibration.json must exist"


def test_no_contaminated_keys():
    """CRITICAL: Fail if ANY non-@b layer data exists in JSON."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    forbidden_patterns = ["@chain", "@q", "@d", "@p", "@C", "@u", "@m",
                          "final_score", "layer_scores", "chain_", "queue_",
                          "downstream_", "upstream_", "composite_"]

    for method_id, method_data in data.items():
        if method_id == "_metadata":
            continue

        for key in method_data:
            for pattern in forbidden_patterns:
                assert pattern not in key.lower(), (
                    f"CONTAMINATION DETECTED: method '{method_id}' contains "
                    f"forbidden key '{key}' matching pattern '{pattern}'. "
                    f"Intrinsic calibration incomplete or contaminated."
                )


def test_only_b_layer_keys():
    """Verify each method entry contains ONLY @b-layer keys."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    allowed_keys = {"intrinsic_score", "b_theory", "b_impl", "b_deploy",
                    "calibration_status", "layer", "last_updated"}

    for method_id, method_data in data.items():
        if method_id == "_metadata":
            continue

        actual_keys = set(method_data.keys())
        extra_keys = actual_keys - allowed_keys
        missing_keys = allowed_keys - actual_keys

        assert not extra_keys, (
            f"Method '{method_id}' has unauthorized keys: {extra_keys}. "
            f"Only {allowed_keys} are allowed."
        )
        assert not missing_keys, (
            f"Method '{method_id}' is missing required keys: {missing_keys}"
        )


def test_coverage_requirement():
    """Verify >=80% coverage (computed methods / total methods)."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    metadata = data["_metadata"]
    total = metadata["total_methods"]
    computed = metadata["computed_methods"]
    coverage = metadata["coverage_percent"]

    assert coverage >= 80.0, (
        f"Coverage requirement FAILED: {coverage}% < 80%. "
        f"Need at least {int(total * 0.8)} computed methods, have {computed}. "
        f"Intrinsic calibration incomplete or contaminated."
    )


def test_minimum_computed_executors():
    """Verify at least 30 executors have status='computed'."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    computed_count = sum(
        1 for method_id, method_data in data.items()
        if method_id != "_metadata" and method_data.get("calibration_status") == "computed"
    )

    assert computed_count >= 30, (
        f"Minimum executor requirement FAILED: {computed_count} < 30 computed methods. "
        f"Intrinsic calibration incomplete or contaminated."
    )


def test_valid_intrinsic_scores():
    """Verify intrinsic_score is [low, high] with valid values."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    for method_id, method_data in data.items():
        if method_id == "_metadata":
            continue

        if method_data.get("calibration_status") == "computed":
            score = method_data.get("intrinsic_score")
            assert isinstance(score, list) and len(score) == 2, (
                f"Method '{method_id}' has invalid intrinsic_score format: {score}"
            )
            assert 0.0 <= score[0] <= 1.0 and 0.0 <= score[1] <= 1.0, (
                f"Method '{method_id}' has intrinsic_score out of range [0,1]: {score}"
            )
            assert score[0] <= score[1], (
                f"Method '{method_id}' has invalid intrinsic_score (low > high): {score}"
            )


def test_valid_b_scores():
    """Verify b_theory, b_impl, b_deploy are valid floats in [0,1]."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    for method_id, method_data in data.items():
        if method_id == "_metadata":
            continue

        if method_data.get("calibration_status") == "computed":
            for b_key in ["b_theory", "b_impl", "b_deploy"]:
                b_val = method_data.get(b_key)
                assert isinstance(b_val, int | float), (
                    f"Method '{method_id}' has invalid {b_key} type: {type(b_val)}"
                )
                assert 0.0 <= b_val <= 1.0, (
                    f"Method '{method_id}' has {b_key} out of range [0,1]: {b_val}"
                )


def test_calibration_status_values():
    """Verify calibration_status is one of: computed, pending, excluded, none."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    valid_statuses = {"computed", "pending", "excluded", "none"}

    for method_id, method_data in data.items():
        if method_id == "_metadata":
            continue

        status = method_data.get("calibration_status")
        assert status in valid_statuses, (
            f"Method '{method_id}' has invalid calibration_status: '{status}'. "
            f"Must be one of {valid_statuses}"
        )


def test_layer_values():
    """Verify layer is one of: engine, processor, utility."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    valid_layers = {"engine", "processor", "utility"}

    for method_id, method_data in data.items():
        if method_id == "_metadata":
            continue

        layer = method_data.get("layer")
        assert layer in valid_layers, (
            f"Method '{method_id}' has invalid layer: '{layer}'. "
            f"Must be one of {valid_layers}"
        )


def test_metadata_structure():
    """Verify _metadata contains required fields."""
    cal_path = Path("config/intrinsic_calibration.json")
    with open(cal_path) as f:
        data = json.load(f)

    assert "_metadata" in data, "JSON must contain _metadata"
    metadata = data["_metadata"]

    required_fields = {"version", "generated", "description", "total_methods",
                      "computed_methods", "coverage_percent"}
    actual_fields = set(metadata.keys())

    missing = required_fields - actual_fields
    assert not missing, f"_metadata missing required fields: {missing}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
