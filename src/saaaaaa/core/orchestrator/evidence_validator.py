from __future__ import annotations

import re
from typing import Any, Iterable


class EvidenceValidator:
    """Validate assembled evidence with configurable rules."""

    @staticmethod
    def validate(evidence: dict[str, Any], validation_rules: list[dict[str, Any]], na_policy: str) -> dict[str, Any]:
        errors: list[str] = []
        warnings: list[str] = []

        for rule in validation_rules:
            field = rule.get("field")
            expected_type = rule.get("type", "any")
            required = rule.get("required", False)
            min_length = rule.get("min_length")
            max_length = rule.get("max_length")
            range_spec = rule.get("range")
            allowed_values = rule.get("allowed_values")
            pattern = rule.get("pattern")

            value = EvidenceValidator._resolve(field, evidence)
            missing = value is None

            if required and missing:
                errors.append(f"Missing required field '{field}'")
                continue
            if missing:
                continue

            if expected_type != "any" and not EvidenceValidator._check_type(value, expected_type):
                errors.append(f"Field '{field}' has incorrect type (expected {expected_type})")
                continue

            if min_length is not None and EvidenceValidator._has_length(value):
                if len(value) < min_length:
                    errors.append(f"Field '{field}' length below min_length {min_length}")
            if max_length is not None and EvidenceValidator._has_length(value):
                if len(value) > max_length:
                    errors.append(f"Field '{field}' length above max_length {max_length}")

            if range_spec and EvidenceValidator._is_number(value):
                low, high = range_spec
                if (low is not None and value < low) or (high is not None and value > high):
                    errors.append(f"Field '{field}' out of range {range_spec}")

            if allowed_values is not None and value not in allowed_values:
                errors.append(f"Field '{field}' not in allowed_values")

            if pattern and isinstance(value, str) and not re.search(pattern, value):
                errors.append(f"Field '{field}' does not match pattern")

        valid = not errors if na_policy == "abort" else True
        if errors and na_policy != "abort":
            warnings.extend(errors)
            errors = []

        if errors and na_policy == "abort":
            raise ValueError(f"Evidence validation failed: {errors}")

        return {"valid": valid, "errors": errors, "warnings": warnings}

    @staticmethod
    def _resolve(path: str, evidence: dict[str, Any]) -> Any:
        if not path:
            return None
        parts = path.split(".")
        current: Any = evidence
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    @staticmethod
    def _check_type(value: Any, expected: str) -> bool:
        mapping = {
            "array": (list, tuple),
            "integer": (int,),
            "float": (float, int),
            "string": (str,),
            "boolean": (bool,),
            "object": (dict,),
            "any": (object,),
        }
        return isinstance(value, mapping.get(expected, (object,)))

    @staticmethod
    def _has_length(value: Any) -> bool:
        return hasattr(value, "__len__")

    @staticmethod
    def _is_number(value: Any) -> bool:
        try:
            float(value)
            return not isinstance(value, bool)
        except (TypeError, ValueError):
            return False
