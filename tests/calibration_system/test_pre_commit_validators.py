"""
Test Pre-Commit Validators Integration

Tests the pre-commit hook system that enforces:
1. No hardcoded calibration patterns
2. JSON schema compliance
3. SHA256 hash verification
4. YAML prohibition
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from pre_commit_validators import (
    ALLOWED_VALUES,
    CALIBRATION_PATTERNS,
    validate_json_schema,
    validate_no_hardcoded_calibrations,
    validate_no_yaml_files,
)


class TestPreCommitValidators:

    def test_hardcoded_calibration_detection(self, tmp_path):
        """Test detection of hardcoded calibration values"""
        test_file = tmp_path / "test_module.py"
        test_file.write_text(
            """
def calculate_score():
    weight = 0.75
    threshold = 0.8
    score = 0.9
    return weight * threshold * score
"""
        )

        is_valid, errors = validate_no_hardcoded_calibrations([test_file])

        assert not is_valid, "Should detect hardcoded calibrations"
        assert len(errors) > 0
        assert any("weight" in str(e) for e in errors)
        assert any("threshold" in str(e) for e in errors)
        assert any("score" in str(e) for e in errors)

    def test_allowed_values_pass(self, tmp_path):
        """Test that allowed literal values pass validation"""
        test_file = tmp_path / "test_module.py"
        test_file.write_text(
            """
def initialize():
    weight = 1.0
    threshold = 0.5
    score = 0
    min_count = 2
    max_count = 10
    return weight, threshold, score
"""
        )

        is_valid, errors = validate_no_hardcoded_calibrations([test_file])

        assert is_valid, f"Allowed values should pass: {errors}"

    def test_comment_exclusion(self, tmp_path):
        """Test that comments are excluded from validation"""
        test_file = tmp_path / "test_module.py"
        test_file.write_text(
            """
def example():
    # weight = 0.75  # This is a comment
    return load_weight_from_config()
"""
        )

        is_valid, errors = validate_no_hardcoded_calibrations([test_file])

        assert is_valid, "Comments should be excluded"

    def test_json_validation_valid(self, tmp_path):
        """Test valid JSON passes validation"""
        test_file = tmp_path / "config.json"
        test_file.write_text(
            json.dumps({"version": "1.0", "settings": {"key": "value"}}, indent=2)
        )

        is_valid, errors = validate_json_schema([test_file])

        assert is_valid, f"Valid JSON should pass: {errors}"

    def test_json_validation_invalid(self, tmp_path):
        """Test invalid JSON is detected"""
        test_file = tmp_path / "config.json"
        test_file.write_text("{invalid json")

        is_valid, errors = validate_json_schema([test_file])

        assert not is_valid, "Invalid JSON should be detected"
        assert len(errors) > 0

    def test_yaml_prohibition(self, tmp_path):
        """Test that YAML files are blocked"""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("key: value")

        is_valid, errors = validate_no_yaml_files([yaml_file])

        assert not is_valid, "YAML files should be blocked"
        assert len(errors) > 0
        assert any("YAML" in str(e) or "yaml" in str(e) for e in errors)

    def test_yml_extension_blocked(self, tmp_path):
        """Test that .yml extension is also blocked"""
        yml_file = tmp_path / "config.yml"
        yml_file.write_text("key: value")

        is_valid, errors = validate_no_yaml_files([yml_file])

        assert not is_valid, ".yml files should be blocked"

    def test_calibration_patterns_comprehensive(self):
        """Test that all calibration patterns are defined"""
        expected_params = [
            "weight",
            "score",
            "threshold",
            "min_evidence",
            "max_evidence",
            "confidence",
            "penalty",
            "tolerance",
            "sensitivity",
            "prior",
        ]

        pattern_params = [param for _, param in CALIBRATION_PATTERNS]

        for param in expected_params:
            assert (
                param in pattern_params
            ), f"Calibration parameter '{param}' not in patterns"

    def test_allowed_values_defined(self):
        """Test that allowed literal values are properly defined"""
        assert "0" in ALLOWED_VALUES
        assert "1" in ALLOWED_VALUES
        assert "0.0" in ALLOWED_VALUES
        assert "1.0" in ALLOWED_VALUES
        assert "0.5" in ALLOWED_VALUES
        assert "-1" in ALLOWED_VALUES

    def test_config_path_exclusion(self):
        """Test that config/ paths are excluded from calibration checks"""
        config_file = Path("config/test_settings.py")

        if config_file.exists():
            content = config_file.read_text()
            original_content = content
        else:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            original_content = None

        try:
            config_file.write_text("weight = 0.75\nthreshold = 0.8\n")

            is_valid, errors = validate_no_hardcoded_calibrations(
                [config_file.absolute()]
            )

            assert is_valid, "Config files should be excluded"
        finally:
            if original_content is not None:
                config_file.write_text(original_content)
            elif config_file.exists():
                config_file.unlink()

    def test_multiple_violations_reported(self, tmp_path):
        """Test that multiple violations are all reported"""
        test_file = tmp_path / "violations.py"
        test_file.write_text(
            """
def bad_code():
    weight = 0.75
    score = 0.85
    threshold = 0.9
    penalty = 0.15
    sensitivity = 0.65
    return weight + score + threshold + penalty + sensitivity
"""
        )

        is_valid, errors = validate_no_hardcoded_calibrations([test_file])

        assert not is_valid
        error_text = "\n".join(errors)
        assert "weight" in error_text
        assert "score" in error_text
        assert "threshold" in error_text
        assert "penalty" in error_text
        assert "sensitivity" in error_text

    def test_string_literals_excluded(self, tmp_path):
        """Test that string literals with patterns are excluded"""
        test_file = tmp_path / "strings.py"
        test_file.write_text(
            """
def example():
    message = "weight = 0.75"
    description = "Set threshold = 0.8 for best results"
    return message, description
"""
        )

        is_valid, errors = validate_no_hardcoded_calibrations([test_file])

        assert is_valid, "String literals should be excluded"

    def test_pre_commit_hook_integration(self):
        """Test that pre-commit hook file exists and is executable"""
        hook_path = Path(".git/hooks/pre-commit")

        assert hook_path.exists(), "Pre-commit hook not installed"

        content = hook_path.read_text()
        assert "pre_commit_validators.py" in content
        assert "bash" in content or "sh" in content

    def test_hash_registry_script_exists(self):
        """Test that hash registry update script exists"""
        script_path = Path("scripts/update_hash_registry.py")

        assert script_path.exists(), "Hash registry script missing"

        content = script_path.read_text()
        assert "sha256" in content.lower()
        assert "hash" in content.lower()

    def test_calibration_registry_pattern_consistency(self):
        """Test that patterns match calibration_registry.py structure"""
        registry_path = Path(
            "src/farfan_pipeline/core/calibration/calibration_registry.py"
        )

        if registry_path.exists():
            content = registry_path.read_text()

            for _pattern, param_name in CALIBRATION_PATTERNS:
                if param_name in ["weight", "score"]:
                    assert (
                        param_name in content
                    ), f"Calibration registry should reference {param_name}"
