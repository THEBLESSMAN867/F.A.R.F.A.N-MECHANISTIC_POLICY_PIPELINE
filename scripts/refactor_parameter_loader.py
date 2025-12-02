#!/usr/bin/env python3
"""Script to refactor all get_parameter_loader() calls to ParameterLoaderV2.get()."""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def refactor_file(file_path: Path) -> Tuple[int, List[str]]:
    """
    Refactor a single file to use ParameterLoaderV2.
    
    Returns:
        Tuple of (replacement_count, issues_list)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    issues = []
    replacements = 0
    
    # Pattern 1: get_parameter_loader().get("method_id").get("param_name", default)
    pattern1 = r'get_parameter_loader\(\)\.get\("([^"]+)"\)\.get\("([^"]+)"(?:,\s*([^)]+))?\)'
    matches1 = list(re.finditer(pattern1, content))
    
    for match in reversed(matches1):
        method_id = match.group(1)
        param_name = match.group(2)
        default = match.group(3) if match.group(3) else "None"
        
        replacement = f'ParameterLoaderV2.get("{method_id}", "{param_name}", {default})'
        content = content[:match.start()] + replacement + content[match.end():]
        replacements += 1
    
    # Pattern 2: _PARAM_LOADER = get_parameter_loader() - remove these global assignments
    pattern2 = r'^\s*_PARAM_LOADER\s*=\s*get_parameter_loader\(\)\s*$'
    if re.search(pattern2, content, re.MULTILINE):
        content = re.sub(pattern2, '', content, flags=re.MULTILINE)
        replacements += 1
    
    # Pattern 3: from farfan_pipeline import get_parameter_loader
    pattern3 = r'from\s+farfan_pipeline\s+import\s+get_parameter_loader\s*\n'
    if re.search(pattern3, content):
        # Replace with ParameterLoaderV2 import
        content = re.sub(
            pattern3,
            'from farfan_pipeline.core.parameters import ParameterLoaderV2\n',
            content
        )
        replacements += 1
    
    # Check if file still has get_parameter_loader references (except in definition)
    remaining = re.findall(r'get_parameter_loader\(\)', content)
    if remaining and '__init__.py' not in str(file_path):
        issues.append(f"Still has {len(remaining)} get_parameter_loader() calls")
    
    # Only write if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return replacements, issues


def main():
    """Main refactoring execution."""
    src_path = Path("src")
    
    if not src_path.exists():
        print("ERROR: src/ directory not found")
        sys.exit(1)
    
    # Find all Python files
    py_files = list(src_path.rglob("*.py"))
    
    # Exclude __init__.py that defines get_parameter_loader
    exclude_files = [
        "src/farfan_pipeline/__init__.py",  # Defines get_parameter_loader
    ]
    
    total_replacements = 0
    total_issues = []
    files_modified = 0
    
    for py_file in py_files:
        if str(py_file) in exclude_files:
            continue
        
        try:
            replacements, issues = refactor_file(py_file)
            if replacements > 0:
                files_modified += 1
                total_replacements += replacements
                print(f"✓ {py_file}: {replacements} replacements")
            
            if issues:
                total_issues.extend([f"{py_file}: {issue}" for issue in issues])
                print(f"  ⚠️  {', '.join(issues)}")
                
        except Exception as e:
            print(f"ERROR processing {py_file}: {e}")
            total_issues.append(f"{py_file}: {str(e)}")
    
    print(f"\n{'='*70}")
    print(f"SUMMARY:")
    print(f"  Files modified: {files_modified}")
    print(f"  Total replacements: {total_replacements}")
    print(f"  Issues: {len(total_issues)}")
    
    if total_issues:
        print(f"\nISSUES:")
        for issue in total_issues[:10]:
            print(f"  - {issue}")
        if len(total_issues) > 10:
            print(f"  ... and {len(total_issues) - 10} more")
    
    return 0 if len(total_issues) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
