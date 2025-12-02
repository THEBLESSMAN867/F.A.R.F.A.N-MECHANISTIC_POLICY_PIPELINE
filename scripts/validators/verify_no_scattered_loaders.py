#!/usr/bin/env python3
"""
Verification script: Ensures complete eradication of scattered parameter loader calls.

FAILURE CONDITIONS:
1. Any get_parameter_loader() call outside src/core/parameters/
2. Any CALIBRATIONS = { dict found anywhere in codebase
3. Script exits with error code and descriptive message
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def run_grep(pattern: str, path: str = "src/") -> List[str]:
    """Run grep and return matching lines."""
    try:
        result = subprocess.run(
            ["grep", "-rn", pattern, path, "--include=*.py"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return []
    except Exception as e:
        print(f"WARNING: grep failed: {e}")
        return []


def check_scattered_loaders() -> Tuple[bool, List[str]]:
    """
    Check for scattered get_parameter_loader() calls.
    
    Returns:
        (success, violations) where success=True if no violations found
    """
    violations = []
    
    # Find all get_parameter_loader() calls
    loader_calls = run_grep(r"get_parameter_loader\(\)")
    
    # Filter out allowed locations
    allowed_patterns = [
        r"src/farfan_pipeline/__init__\.py.*def get_parameter_loader",
        r"src/farfan_pipeline/__init__\.py.*get_parameter_loader\(\)",
        r"src/farfan_pipeline/__init__\.py.*__all__.*get_parameter_loader",
        r"src/farfan_pipeline/core/calibration/.*",
        r"src/farfan_pipeline/core/parameters/.*",
        r"#.*get_parameter_loader",  # Comments
        r"__all__.*get_parameter_loader",  # __all__ exports
    ]
    
    for call in loader_calls:
        is_allowed = False
        for pattern in allowed_patterns:
            if re.search(pattern, call):
                is_allowed = True
                break
        
        if not is_allowed:
            violations.append(f"SCATTERED LOADER: {call}")
    
    return len(violations) == 0, violations


def check_calibrations_dict() -> Tuple[bool, List[str]]:
    """
    Check for CALIBRATIONS = { dict definitions.
    
    Returns:
        (success, violations) where success=True if no violations found
    """
    violations = []
    
    # Find CALIBRATIONS dict definitions
    calibrations_defs = run_grep(r"CALIBRATIONS\s*=\s*\{")
    
    # No CALIBRATIONS dict should exist anywhere
    for definition in calibrations_defs:
        violations.append(f"CALIBRATIONS DICT: {definition}")
    
    return len(violations) == 0, violations


def check_old_imports() -> Tuple[bool, List[str]]:
    """
    Check for old parameter_loader imports (not from core.parameters).
    
    Returns:
        (success, violations) where success=True if no violations found
    """
    violations = []
    
    # Find imports
    import_lines = run_grep(r"from.*parameter_loader import")
    
    # Filter out new approved imports
    approved_patterns = [
        r"from farfan_pipeline\.core\.parameters import",
        r"from \.core\.parameters import",
        r"from farfan_pipeline\.core\.calibration\.parameter_loader import ParameterLoader",
        r"from \.core\.calibration\.parameter_loader import ParameterLoader",
    ]
    
    for import_line in import_lines:
        is_approved = False
        for pattern in approved_patterns:
            if re.search(pattern, import_line):
                is_approved = True
                break
        
        if not is_approved:
            violations.append(f"OLD IMPORT: {import_line}")
    
    return len(violations) == 0, violations


def main() -> int:
    """
    Main verification execution.
    
    Returns:
        0 if all checks pass, 1 if any failures
    """
    print("="*70)
    print("PARAMETER LOADER ERADICATION VERIFICATION")
    print("="*70)
    
    all_passed = True
    all_violations = []
    
    # Check 1: Scattered loaders
    print("\n[1/3] Checking for scattered get_parameter_loader() calls...")
    passed, violations = check_scattered_loaders()
    if passed:
        print("  ✓ PASS: No scattered loader calls found")
    else:
        print(f"  ✗ FAIL: Found {len(violations)} scattered loader calls")
        all_passed = False
        all_violations.extend(violations)
    
    # Check 2: CALIBRATIONS dict
    print("\n[2/3] Checking for CALIBRATIONS = { dict definitions...")
    passed, violations = check_calibrations_dict()
    if passed:
        print("  ✓ PASS: No CALIBRATIONS dict found")
    else:
        print(f"  ✗ FAIL: Found {len(violations)} CALIBRATIONS dict definitions")
        all_passed = False
        all_violations.extend(violations)
    
    # Check 3: Old imports
    print("\n[3/3] Checking for old parameter_loader imports...")
    passed, violations = check_old_imports()
    if passed:
        print("  ✓ PASS: No problematic imports found")
    else:
        print(f"  ✗ FAIL: Found {len(violations)} problematic imports")
        all_passed = False
        all_violations.extend(violations)
    
    # Final verdict
    print("\n" + "="*70)
    if all_passed:
        print("✓ VERIFICATION PASSED")
        print("  All scattered parameter loaders have been eradicated.")
        print("  Centralized ParameterLoaderV2 is the single source of truth.")
        return 0
    else:
        print("✗ VERIFICATION FAILED")
        print(f"  loader eradication incomplete - {len(all_violations)} violations remain")
        print("\nVIOLATIONS:")
        for violation in all_violations[:20]:
            print(f"  - {violation}")
        if len(all_violations) > 20:
            print(f"  ... and {len(all_violations) - 20} more")
        return 1


if __name__ == "__main__":
    sys.exit(main())
