#!/usr/bin/env python3
"""Validator to ensure no relative imports exist in farfan_pipeline.

This script enforces the absolute-imports-only policy by scanning all Python
files in src/farfan_pipeline/ and failing if any relative imports are found.

Exit codes:
    0: No relative imports found (success)
    1: Relative imports found (failure)
    2: Script error (e.g., directory not found)

Usage:
    python scripts/validators/validate_no_relative_imports.py
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple


def find_relative_imports(file_path: Path) -> List[Tuple[int, str]]:
    """Find all relative imports in a Python file.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        List of (line_number, import_statement) tuples for relative imports
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"⚠️  Could not parse {file_path}: {e}", file=sys.stderr)
        return []
    
    violations = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.ImportFrom,)):
            # ImportFrom with level > 0 indicates relative import
            if hasattr(node, 'level') and node.level and node.level > 0:
                line_text = content.split('\n')[node.lineno - 1].strip()
                violations.append((node.lineno, line_text))
    
    return violations


def main() -> int:
    """Scan farfan_pipeline for relative imports and report violations."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    src_dir = repo_root / "src" / "farfan_pipeline"
    
    if not src_dir.exists():
        print(f"❌ Source directory not found: {src_dir}", file=sys.stderr)
        return 2
    
    print("🔍 Scanning for relative imports in farfan_pipeline...")
    print(f"   Root: {src_dir}\n")
    
    all_violations = []
    
    for py_file in src_dir.rglob("*.py"):
        violations = find_relative_imports(py_file)
        if violations:
            all_violations.append((py_file, violations))
    
    if not all_violations:
        print("✅ No relative imports found. All imports are absolute.")
        return 0
    
    print(f"❌ Found relative imports in {len(all_violations)} file(s):\n")
    
    for file_path, violations in all_violations:
        rel_path = file_path.relative_to(repo_root)
        print(f"  {rel_path}:")
        for line_num, line_text in violations:
            print(f"    Line {line_num}: {line_text}")
        print()
    
    print("Policy violation: All imports must be absolute.")
    print("Example: Use 'from farfan_pipeline.core import x' instead of 'from . import x'")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
