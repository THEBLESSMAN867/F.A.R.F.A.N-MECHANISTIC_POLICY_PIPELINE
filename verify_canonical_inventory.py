#!/usr/bin/env python3
"""Verify the structure of generated canonical inventory files."""

import json
import sys


def verify_canonical_inventory():
    print("Verifying canonical_method_inventory.json...")
    with open("canonical_method_inventory.json") as f:
        data = json.load(f)

    assert "methods" in data, "Missing 'methods' key"
    assert "metadata" in data, "Missing 'metadata' key"

    metadata = data["metadata"]
    assert "total_methods" in metadata
    assert "scan_timestamp" in metadata
    assert "source_directory" in metadata

    methods = data["methods"]
    assert len(methods) > 0, "No methods found"

    sample_method = next(iter(methods.values()))
    required_keys = [
        "canonical_name",
        "file_path",
        "line_number",
        "class_name",
        "role",
        "is_executor",
        "signature",
    ]
    for key in required_keys:
        assert key in sample_method, f"Missing key '{key}' in method"

    assert (
        "parameters" in sample_method["signature"]
    ), "Missing 'parameters' in signature"

    print(f"  ✓ Valid structure with {len(methods)} methods")
    return True


def verify_statistics():
    print("Verifying method_statistics.json...")
    with open("method_statistics.json") as f:
        data = json.load(f)

    required_keys = [
        "total_methods",
        "total_executors",
        "by_role",
        "by_module",
        "executor_distribution",
    ]
    for key in required_keys:
        assert key in data, f"Missing key '{key}'"

    assert data["total_methods"] > 0
    assert data["total_executors"] >= 0
    assert len(data["by_role"]) > 0
    assert len(data["by_module"]) > 0

    print("  ✓ Valid structure")
    print(f"    Total methods: {data['total_methods']}")
    print(f"    Total executors: {data['total_executors']}")
    print(f"    Roles: {list(data['by_role'].keys())}")
    return True


def verify_excluded():
    print("Verifying excluded_methods.json...")
    with open("excluded_methods.json") as f:
        data = json.load(f)

    assert "excluded_methods" in data, "Missing 'excluded_methods' key"
    assert "exclusion_reason" in data, "Missing 'exclusion_reason' key"
    assert "total_excluded" in data, "Missing 'total_excluded' key"

    assert data["exclusion_reason"] == "never calibrate"
    assert data["total_excluded"] == len(data["excluded_methods"])

    if len(data["excluded_methods"]) > 0:
        sample = data["excluded_methods"][0]
        required_keys = [
            "canonical_id",
            "reason",
            "method_name",
            "file_path",
            "line_number",
        ]
        for key in required_keys:
            assert key in sample, f"Missing key '{key}' in excluded method"

    print(f"  ✓ Valid structure with {data['total_excluded']} excluded methods")
    return True


def main():
    try:
        verify_canonical_inventory()
        verify_statistics()
        verify_excluded()
        print("\n✅ All files verified successfully!")
        return 0
    except Exception as e:
        print(f"\n❌ Verification failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
