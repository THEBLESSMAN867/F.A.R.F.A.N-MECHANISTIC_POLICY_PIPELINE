# Pre-Commit Hook Quick Reference

## Testing the Hook

```bash
# Run validator tests
pytest tests/calibration_system/test_pre_commit_validators.py -v

# Run integration tests
pytest tests/calibration_system/test_no_hardcoded_calibrations.py -v

# Test hook manually (create test violation)
echo "weight = 0.75" > test_violation.py
git add test_violation.py
git commit -m "Test" # Should be BLOCKED
git reset HEAD test_violation.py && rm test_violation.py
```

## Updating Config Files

```bash
# 1. Edit config
vim config/intrinsic_calibration.json

# 2. Update hash registry
python scripts/update_hash_registry.py

# 3. Commit both
git add config/intrinsic_calibration.json scripts/config_hash_registry.json
git commit -m "Update calibration config"
```

## What Gets Blocked

❌ `weight = 0.75` (except in config/ or allowed values: 0, 1, 0.5, 0.0, 1.0, -1, 2, 10, 100)
❌ `threshold = 0.8`
❌ `score = 0.9`
❌ `*.yaml`, `*.yml` files
❌ Config JSON modified without updating hash registry

✓ `weight = 1.0` (allowed value)
✓ `weight = load_from_config()`
✓ Files in `config/`, `system/config/`, `test/`
✓ JSON files (with valid structure)

## Emergency Bypass

```bash
git commit --no-verify -m "Emergency fix"
```

**WARNING**: Use only in true emergencies. Bypassing the hook risks calibration integrity.

## Hook Location

- Hook: `.git/hooks/pre-commit`
- Validators: `scripts/pre_commit_validators.py`
- Hash registry: `scripts/config_hash_registry.json`
- Hash updater: `scripts/update_hash_registry.py`
- Tests: `tests/calibration_system/test_pre_commit_validators.py`
- Documentation: `scripts/README_PRE_COMMIT.md`
