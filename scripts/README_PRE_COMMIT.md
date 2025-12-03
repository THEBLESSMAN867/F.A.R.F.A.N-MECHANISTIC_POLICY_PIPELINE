# Pre-Commit Hook System for FARFAN Calibration Integrity

## Overview

The pre-commit hook system enforces critical constraints to maintain calibration system integrity:

1. **No Hardcoded Calibrations**: Blocks commits containing `weight=`, `score=`, `threshold=` with numeric literals (except allowed values: 0, 1, 0.0, 1.0, 0.5, -1, 2, 10, 100)
2. **JSON Schema Compliance**: Validates all config JSON files against their schemas
3. **SHA256 Hash Verification**: Ensures config file modifications update the hash registry
4. **YAML Prohibition**: Blocks any YAML files (`.yaml`, `.yml`) from being committed

## Installation

The pre-commit hook is automatically installed at `.git/hooks/pre-commit`. It runs on every commit attempt.

To verify installation:
```bash
test -x .git/hooks/pre-commit && echo "✓ Installed" || echo "✗ Not installed"
```

## Components

### 1. Pre-Commit Hook (`.git/hooks/pre-commit`)
- Shell script that runs on `git commit`
- Calls Python validators on staged files
- Exits with non-zero status to block commit if violations found

### 2. Validator Module (`scripts/pre_commit_validators.py`)
- Main validation logic
- Four independent validators
- Returns detailed error messages for violations

### 3. Hash Registry (`scripts/config_hash_registry.json`)
- SHA256 checksums for all config JSON files
- Tracks file size and last update timestamp
- Updated via `update_hash_registry.py`

### 4. Hash Update Script (`scripts/update_hash_registry.py`)
- Scans `config/` and `system/config/` directories
- Computes SHA256 hashes for all JSON files
- Updates registry with new checksums

## Usage

### Normal Commits
The hook runs automatically:
```bash
git add src/module.py
git commit -m "Add feature"
# Hook validates automatically
```

### When Validation Fails

#### Hardcoded Calibration Detected
```
COMMIT BLOCKED: Hardcoded calibration values detected

Found hardcoded calibration patterns:

  src/module.py:15: Hardcoded weight=0.75
    Line: weight = 0.75
    Calibration values must be loaded from config files.

All calibration parameters must be externalized to:
  - config/intrinsic_calibration.json
  - system/config/calibration/intrinsic_calibration.json
```

**Fix**: Move the value to a config file and load it:
```python
# Bad
def calculate():
    weight = 0.75  # ✗ Blocked
    
# Good
from calibration_registry import resolve_calibration
def calculate():
    cal = resolve_calibration("MyClass", "my_method")
    weight = cal.aggregation_weight  # ✓ Allowed
```

#### Config Modified Without Hash Update
```
COMMIT BLOCKED: SHA256 hash mismatch

Config files modified without updating hash registry:

  config/intrinsic_calibration.json:
    Expected SHA256: abc123...
    Actual SHA256:   def456...

Update the hash registry with:
  python scripts/update_hash_registry.py
```

**Fix**: Update the registry after config changes:
```bash
# Edit config file
vim config/intrinsic_calibration.json

# Update hash registry
python scripts/update_hash_registry.py

# Commit both
git add config/intrinsic_calibration.json scripts/config_hash_registry.json
git commit -m "Update calibration config"
```

#### YAML File Detected
```
COMMIT BLOCKED: YAML files are prohibited

Detected YAML files:
  config/settings.yaml

FARFAN uses JSON exclusively for configuration.
Convert YAML to JSON before committing.
```

**Fix**: Convert to JSON:
```bash
# Convert YAML to JSON
python -c "import json, yaml; print(json.dumps(yaml.safe_load(open('config/settings.yaml')), indent=2))" > config/settings.json

# Remove YAML file
git rm config/settings.yaml
git add config/settings.json
```

### Updating Config Files Workflow

1. **Edit config file**:
   ```bash
   vim config/intrinsic_calibration.json
   ```

2. **Update hash registry**:
   ```bash
   python scripts/update_hash_registry.py
   ```

3. **Commit both files**:
   ```bash
   git add config/intrinsic_calibration.json scripts/config_hash_registry.json
   git commit -m "Update calibration: increase threshold for method X"
   ```

### Bypassing the Hook (Emergency Only)

If you need to bypass the hook temporarily:
```bash
git commit --no-verify -m "Emergency fix"
```

**WARNING**: Only use `--no-verify` in emergencies. Bypassing validation can corrupt calibration integrity.

## Allowed Literal Values

These numeric literals are allowed in code without triggering violations:
- `0`, `0.0` - Zero values
- `1`, `1.0` - Unity values
- `0.5` - Half value
- `-1` - Negative one (common sentinel)
- `2`, `10`, `100` - Common integer constants

All other numeric literals assigned to calibration parameters must come from config files.

## Excluded Paths

These paths are excluded from validation:
- `test/`, `tests/` - Test files
- `config/`, `system/config/` - Config files themselves
- `__pycache__/`, `.git/` - Build/system directories
- `venv/`, `.venv/`, `farfan-env/` - Virtual environments
- `node_modules/`, `.eggs/`, `dist/`, `build/` - Package artifacts

## Testing

### Run Test Suite
```bash
# Test the pre-commit validators
pytest tests/calibration_system/test_pre_commit_validators.py -v

# Test no hardcoded calibrations (includes pre-commit integration tests)
pytest tests/calibration_system/test_no_hardcoded_calibrations.py -v
```

### Manual Testing
```bash
# Create a test file with violations
echo 'weight = 0.75' > test_violation.py
git add test_violation.py

# Try to commit (should be blocked)
git commit -m "Test violation"

# Clean up
git reset HEAD test_violation.py
rm test_violation.py
```

## Integration with CI/CD

The same validation logic should run in CI:

```yaml
# .github/workflows/calibration-integrity.yml
- name: Validate No Hardcoded Calibrations
  run: |
    python scripts/pre_commit_validators.py
    pytest tests/calibration_system/test_no_hardcoded_calibrations.py -v
```

## Troubleshooting

### Hook Not Running
```bash
# Check if hook exists and is executable
ls -la .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### False Positives

If legitimate code is flagged:

1. Check if value is in ALLOWED_VALUES (0, 1, 0.5, etc.)
2. Ensure parameter name matches patterns exactly
3. Add to exclusion list if necessary (edit `scripts/pre_commit_validators.py`)

### Hash Registry Out of Sync

If hash validation fails after legitimate changes:
```bash
# Regenerate entire registry
python scripts/update_hash_registry.py

# Verify changes
git diff scripts/config_hash_registry.json

# Commit registry update
git add scripts/config_hash_registry.json
git commit -m "Update hash registry"
```

## Architecture

```
.git/hooks/pre-commit (Shell)
    ↓
scripts/pre_commit_validators.py (Python)
    ↓
    ├─> validate_no_hardcoded_calibrations()
    ├─> validate_json_schema()
    ├─> validate_sha256_hashes() → scripts/config_hash_registry.json
    └─> validate_no_yaml_files()
```

## Calibration Pattern Reference

Protected parameter patterns:
```python
weight = <number>       # Aggregation weights
score = <number>        # Scoring values  
threshold = <number>    # Decision thresholds
min_evidence = <int>    # Evidence minimums
max_evidence = <int>    # Evidence maximums
confidence = <number>   # Confidence levels
penalty = <number>      # Penalty factors
tolerance = <number>    # Tolerance levels
sensitivity = <number>  # Sensitivity parameters
prior = <number>        # Bayesian priors
```

All must be loaded from:
- `config/intrinsic_calibration.json`
- `system/config/calibration/intrinsic_calibration.json`
- Via `calibration_registry.resolve_calibration()`

## Maintenance

### Adding New Calibration Patterns

Edit `scripts/pre_commit_validators.py`:
```python
CALIBRATION_PATTERNS = [
    (r'\bweight\s*=\s*([0-9]+\.?[0-9]*)', 'weight'),
    (r'\bnew_param\s*=\s*([0-9]+\.?[0-9]*)', 'new_param'),  # Add here
    # ...
]
```

### Updating Allowed Values

Edit `scripts/pre_commit_validators.py`:
```python
ALLOWED_VALUES = {'0', '1', '0.0', '1.0', '0.5', '-1', '2', '10', '100', '42'}  # Add here
```

### Adding Schema Definitions

Edit `scripts/pre_commit_validators.py`:
```python
JSON_SCHEMA_DEFINITIONS = {
    'intrinsic_calibration.json': { ... },
    'new_config.json': {  # Add here
        'type': 'object',
        'properties': { ... }
    }
}
```

## Support

For issues or questions:
1. Check this README
2. Run tests: `pytest tests/calibration_system/ -v`
3. Inspect hook: `cat .git/hooks/pre-commit`
4. Review validator: `cat scripts/pre_commit_validators.py`
