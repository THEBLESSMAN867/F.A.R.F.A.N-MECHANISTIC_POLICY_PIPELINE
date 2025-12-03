#!/usr/bin/env python3
"""Pre-commit validators for FARFAN calibration system integrity.

This module provides validation functions that enforce critical constraints:
1. No hardcoded calibration patterns (weight=, score=, threshold= with numeric literals)
2. JSON schema compliance for all config files
3. SHA256 hash verification against registry
4. YAML prohibition enforcement
"""

import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CALIBRATION_PATTERNS = [
    (r"\bweight\s*=\s*([0-9]+\.?[0-9]*)", "weight"),
    (r"\bscore\s*=\s*([0-9]+\.?[0-9]*)", "score"),
    (r"\bthreshold\s*=\s*([0-9]+\.?[0-9]*)", "threshold"),
    (r"\bmin_evidence\s*=\s*([0-9]+)", "min_evidence"),
    (r"\bmax_evidence\s*=\s*([0-9]+)", "max_evidence"),
    (r"\bconfidence\s*=\s*([0-9]+\.?[0-9]*)", "confidence"),
    (r"\bpenalty\s*=\s*([0-9]+\.?[0-9]*)", "penalty"),
    (r"\btolerance\s*=\s*([0-9]+\.?[0-9]*)", "tolerance"),
    (r"\bsensitivity\s*=\s*([0-9]+\.?[0-9]*)", "sensitivity"),
    (r"\bprior\s*=\s*([0-9]+\.?[0-9]*)", "prior"),
]

ALLOWED_VALUES = {"0", "1", "0.0", "1.0", "0.5", "-1", "2", "10", "100"}

EXCLUDED_PATH_SEGMENTS = [
    "__pycache__",
    ".git",
    "farfan-env",
    "venv",
    ".venv",
    "node_modules",
    ".eggs",
    "dist",
    "build",
]

EXCLUDED_PATH_PREFIXES = ["/test/", "/tests/", "config/", "system/config/"]

HASH_REGISTRY_FILE = REPO_ROOT / "scripts" / "config_hash_registry.json"

JSON_SCHEMA_DEFINITIONS = {
    "intrinsic_calibration.json": {
        "type": "object",
        "properties": {
            "_metadata": {"type": "object"},
        },
        "additionalProperties": {
            "type": "object",
            "properties": {
                "intrinsic_score": {"type": "array"},
                "b_theory": {"type": "number"},
                "b_impl": {"type": "number"},
                "b_deploy": {"type": "number"},
                "calibration_status": {"type": "string"},
                "layer": {"type": "string"},
                "last_updated": {"type": "string"},
            },
        },
    }
}


def is_excluded_path(file_path: Path) -> bool:
    """Check if file should be excluded from validation."""
    path_str = str(file_path)

    if "/tmp" in path_str or "/private/var" in path_str:
        return False

    try:
        rel_path = str(file_path.relative_to(REPO_ROOT))
    except ValueError:
        return False

    for segment in EXCLUDED_PATH_SEGMENTS:
        if segment in rel_path:
            return True

    for prefix in EXCLUDED_PATH_PREFIXES:
        if rel_path.startswith(prefix) or f"/{prefix}" in rel_path:
            return True

    return False


def is_comment_or_string(line: str) -> bool:
    """Check if line is a comment, docstring, or inside string literal."""
    stripped = line.strip()

    if stripped.startswith("#"):
        return True

    if stripped.startswith('"""') or stripped.startswith("'''"):
        return True

    min_quote_count = 2
    return (
        stripped.count('"') >= min_quote_count or stripped.count("'") >= min_quote_count
    )


def validate_no_hardcoded_calibrations(
    staged_files: list[Path],
) -> tuple[bool, list[str]]:
    """Validate that no hardcoded calibration patterns exist in staged Python files.

    Args:
        staged_files: List of staged file paths

    Returns:
        Tuple of (is_valid, error_messages)
    """
    violations = []

    for file_path in staged_files:
        if not str(file_path).endswith(".py"):
            continue

        if is_excluded_path(file_path):
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            for lineno, line in enumerate(lines, 1):
                if is_comment_or_string(line):
                    continue

                for pattern, param_name in CALIBRATION_PATTERNS:
                    matches = re.finditer(pattern, line)

                    for match in matches:
                        value = match.group(1)

                        if value not in ALLOWED_VALUES:
                            violations.append(
                                f"{file_path}:{lineno}: Hardcoded {param_name}={value}\n"
                                f"  Line: {line.strip()}\n"
                                f"  Calibration values must be loaded from config files."
                            )

        except (UnicodeDecodeError, OSError) as e:
            violations.append(f"Error reading {file_path}: {e}")

    if violations:
        error_msg = (
            [
                "=" * 80,
                "COMMIT BLOCKED: Hardcoded calibration values detected",
                "=" * 80,
                "",
                "Found hardcoded calibration patterns:",
                "",
            ]
            + violations
            + [
                "",
                "All calibration parameters must be externalized to:",
                "  - config/intrinsic_calibration.json",
                "  - system/config/calibration/intrinsic_calibration.json",
                "  - src/farfan_pipeline/core/calibration/calibration_registry.py",
                "",
                "Allowed literal values: 0, 1, 0.0, 1.0, 0.5, -1, 2, 10, 100",
                "=" * 80,
            ]
        )
        return False, error_msg

    return True, []


def validate_json_schema(staged_files: list[Path]) -> tuple[bool, list[str]]:
    """Validate JSON files against their schemas.

    Args:
        staged_files: List of staged file paths

    Returns:
        Tuple of (is_valid, error_messages)
    """
    violations = []

    for file_path in staged_files:
        if not str(file_path).endswith(".json"):
            continue

        if is_excluded_path(file_path):
            continue

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            file_name = file_path.name
            if file_name in JSON_SCHEMA_DEFINITIONS:
                schema = JSON_SCHEMA_DEFINITIONS[file_name]
                if not _validate_against_schema(data, schema):
                    violations.append(f"{file_path}: JSON schema validation failed")

        except json.JSONDecodeError as e:
            violations.append(f"{file_path}: Invalid JSON - {e}")
        except Exception as e:
            violations.append(f"{file_path}: Validation error - {e}")

    if violations:
        error_msg = (
            [
                "=" * 80,
                "COMMIT BLOCKED: JSON schema validation failed",
                "=" * 80,
                "",
            ]
            + violations
            + [
                "",
                "Fix JSON schema compliance before committing.",
                "=" * 80,
            ]
        )
        return False, error_msg

    return True, []


def _validate_against_schema(data: dict, schema: dict) -> bool:
    """Basic schema validation (simplified)."""
    if schema.get("type") == "object":
        if not isinstance(data, dict):
            return False

        required = schema.get("required", [])
        for req_field in required:
            if req_field not in data:
                return False

    return True


def validate_sha256_hashes(staged_files: list[Path]) -> tuple[bool, list[str]]:
    """Validate that config file SHA256 hashes match registry.

    Args:
        staged_files: List of staged file paths

    Returns:
        Tuple of (is_valid, error_messages)
    """
    if not HASH_REGISTRY_FILE.exists():
        return True, []

    try:
        with open(HASH_REGISTRY_FILE, encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        return False, [f"Error loading hash registry: {e}"]

    violations = []

    for file_path in staged_files:
        if not (str(file_path).endswith(".json") and "config" in str(file_path)):
            continue

        if is_excluded_path(file_path):
            continue

        rel_path = str(file_path.relative_to(REPO_ROOT))

        if rel_path in registry:
            try:
                with open(file_path, "rb") as f:
                    actual_hash = hashlib.sha256(f.read()).hexdigest()

                expected_hash = registry[rel_path]["sha256"]

                if actual_hash != expected_hash:
                    violations.append(
                        f"{file_path}:\n"
                        f"  Expected SHA256: {expected_hash}\n"
                        f"  Actual SHA256:   {actual_hash}\n"
                        f"  Config file modified without updating registry."
                    )

            except Exception as e:
                violations.append(f"{file_path}: Error computing hash - {e}")

    if violations:
        error_msg = (
            [
                "=" * 80,
                "COMMIT BLOCKED: SHA256 hash mismatch",
                "=" * 80,
                "",
                "Config files modified without updating hash registry:",
                "",
            ]
            + violations
            + [
                "",
                "Update the hash registry with:",
                "  python scripts/update_hash_registry.py",
                "=" * 80,
            ]
        )
        return False, error_msg

    return True, []


def validate_no_yaml_files(staged_files: list[Path]) -> tuple[bool, list[str]]:
    """Validate that no YAML files are being committed.

    Args:
        staged_files: List of staged file paths

    Returns:
        Tuple of (is_valid, error_messages)
    """
    yaml_files = []

    for file_path in staged_files:
        if is_excluded_path(file_path):
            continue

        if str(file_path).endswith((".yaml", ".yml")):
            yaml_files.append(str(file_path))

    if yaml_files:
        error_msg = (
            [
                "=" * 80,
                "COMMIT BLOCKED: YAML files are prohibited",
                "=" * 80,
                "",
                "Detected YAML files:",
                "",
            ]
            + [f"  {f}" for f in yaml_files]
            + [
                "",
                "FARFAN uses JSON exclusively for configuration.",
                "Convert YAML to JSON before committing.",
                "=" * 80,
            ]
        )
        return False, error_msg

    return True, []


def main():
    """Run all pre-commit validators."""
    import subprocess

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print("Error: Could not get staged files")
        return 1

    staged_files = [REPO_ROOT / f for f in result.stdout.strip().split("\n") if f]

    if not staged_files:
        return 0

    all_valid = True
    all_errors = []

    validators = [
        ("Hardcoded Calibrations", validate_no_hardcoded_calibrations),
        ("JSON Schema", validate_json_schema),
        ("SHA256 Hashes", validate_sha256_hashes),
        ("YAML Prohibition", validate_no_yaml_files),
    ]

    for _name, validator in validators:
        is_valid, errors = validator(staged_files)
        if not is_valid:
            all_valid = False
            all_errors.extend(errors)

    if not all_valid:
        print("\n".join(all_errors), file=sys.stderr)
        return 1

    print("✓ All pre-commit validations passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
