#!/usr/bin/env python3
"""
Validate GitHub Actions workflow YAML files
"""
import sys
import yaml
from pathlib import Path

def validate_workflow(filepath):
    """Validate a single workflow YAML file."""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check required fields
        if 'name' not in data:
            print(f"❌ {filepath.name}: Missing 'name' field")
            return False
        
        if 'on' not in data:
            print(f"❌ {filepath.name}: Missing 'on' field")
            return False
        
        if 'jobs' not in data:
            print(f"❌ {filepath.name}: Missing 'jobs' field")
            return False
        
        print(f"✅ {filepath.name}: Valid workflow")
        print(f"   Name: {data['name']}")
        print(f"   Jobs: {', '.join(data['jobs'].keys())}")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ {filepath.name}: YAML syntax error")
        print(f"   {e}")
        return False
    except Exception as e:
        print(f"❌ {filepath.name}: Error - {e}")
        return False

def main():
    workflows_dir = Path('.github/workflows')
    
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        sys.exit(1)
    
    print("=== Validating GitHub Actions Workflows ===\n")
    
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print("❌ No workflow files found")
        sys.exit(1)
    
    results = []
    for workflow_file in sorted(workflow_files):
        result = validate_workflow(workflow_file)
        results.append(result)
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} workflows valid")
    
    if passed == total:
        print("✅ All workflows are valid!")
        sys.exit(0)
    else:
        print("❌ Some workflows have errors")
        sys.exit(1)

if __name__ == '__main__':
    main()
