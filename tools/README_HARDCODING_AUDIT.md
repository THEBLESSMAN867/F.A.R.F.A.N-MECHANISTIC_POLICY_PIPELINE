# Hardcoding Audit Scanner

## Overview

The Hardcoding Audit Scanner (`hardcoding_audit_scanner.py`) is a comprehensive tool for detecting calibration hardcoding violations in the FARFAN pipeline codebase.

## Purpose

This scanner enforces the architectural principle that **all calibration values must be externalized to JSON configuration files**, preventing hardcoding that undermines reproducibility, auditability, and maintainability.

## Detected Violations

### 1. Hardcoded Calibration Values
Detects numeric literals assigned to variables with calibration-related names:
- `score`, `weight`, `threshold`, `coefficient`
- `b_theory`, `b_impl`, `b_deploy`
- `alpha`, `beta`, `gamma`, `prior`
- Layer scores: `@b`, `@chain`, `@q`, `@d`, `@p`, `@C`, `@u`, `@m`

**Example Violation:**
```python
CALIBRATION_THRESHOLD = 0.7  # ❌ Hardcoded
score = 0.65                  # ❌ Hardcoded
```

**Correct Approach:**
```python
# Load from config/intrinsic_calibration.json
threshold = config["calibration_threshold"]
score = orchestrator.calibrate_method(method_id, context)
```

### 2. Inline Calibration Dictionaries
Detects dict/JSON literals containing calibration data:

**Example Violation:**
```python
weights = {
    "quality": 0.5,      # ❌ Inline calibration dict
    "provenance": 0.5
}
```

**Correct Approach:**
```python
# Load from config/contextual_parametrization.json
weights = loader.get_layer_weights(method_role)
```

### 3. YAML File References (PROHIBITED)
YAML is a **prohibited format** for calibration data due to:
- Lack of strict schema validation
- Ambiguous type coercion
- Inconsistent parsing behavior

**Example Violation:**
```python
with open("config.yaml") as f:  # ❌ YAML prohibited
    config = yaml.safe_load(f)
```

**Correct Approach:**
```python
with open("config.json") as f:  # ✅ Use JSON
    config = json.load(f)
```

### 4. Undeclared Bayesian Priors
Detects Bayesian priors that lack explicit documentation:

**Example Violation:**
```python
prior = scipy.stats.beta(a=2, b=5)  # ❌ Undeclared prior
```

**Correct Approach:**
```python
# Document in config/bayesian_priors.json with justification
prior_params = config["priors"]["evidence_strength"]
prior = scipy.stats.beta(
    a=prior_params["alpha"],
    b=prior_params["beta"]
)
```

## Usage

### Basic Scan
```bash
python tools/hardcoding_audit_scanner.py
```

This will:
1. Scan all Python files in `src/farfan_pipeline/`
2. Detect violations using both AST and regex analysis
3. Generate `violations_audit.md` with detailed findings
4. Exit with code 1 if CRITICAL violations found

### Output

The scanner generates `violations_audit.md` containing:

1. **Executive Summary**: Violation counts by severity
2. **Violation Categories**: Breakdown by type
3. **Known Violators**: Priority review of specified files
   - `orchestrator.py` lines 232-271
   - `layer_computers.py` lines 141-156
4. **Detailed Violations**: File-by-file analysis with code context
5. **YAML References**: List of files referencing prohibited format
6. **Remediation Recommendations**: Step-by-step fix guidance

### Report Format

Each violation includes:
- **File path**: Full path to violating file
- **Line number**: Exact line of violation
- **Violation type**: Category of violation
- **Severity**: CRITICAL, HIGH, MEDIUM, LOW
- **Code snippet**: Context with 2 lines before/after
- **Context**: Additional explanation

**Example:**
```markdown
### src/farfan_pipeline/core/calibration/orchestrator.py

**Line 232** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'score' assigned hardcoded value: 0.65

```python
     230:     def _compute_chain_score(self, context: CalibrationContext) -> float:
     231:         """Compute chain of evidence score (@chain)."""
>>>  232:         score = 0.65
     233:         if context.dimension > 0:
     234:             score += 0.15 * min(context.dimension / 10.0, 1.0)
```

## Detection Methods

### 1. AST-Based Detection
Uses Python's Abstract Syntax Tree parser to detect:
- Variable assignments to calibration-named variables
- Dict literals with calibration keys
- Function calls to `json.loads()` with inline JSON
- Bayesian prior declarations

### 2. Regex Pattern Matching
Complements AST analysis with pattern matching for:
- Calibration value assignments
- Layer score operators (`@b`, `@chain`, etc.)
- YAML file extensions (`.yaml`, `.yml`)
- Choquet weight patterns
- scipy.stats distributions

## Severity Levels

- **CRITICAL**: Violations that completely break calibration architecture
  - YAML references
  - Inline JSON with calibration data

- **HIGH**: Direct hardcoding that bypasses configuration
  - Hardcoded calibration values
  - Inline calibration dictionaries

- **MEDIUM**: Indirect or potential violations
  - Pattern matches that may be false positives
  - Undeclared Bayesian priors

- **LOW**: Parse errors or scan issues
  - Syntax errors preventing analysis

## Remediation Steps

### Step 1: Move Values to Config Files

**For @b scores:**
```json
// config/intrinsic_calibration.json
{
  "methods": {
    "method_id_001": {
      "b_theory": 0.85,
      "b_impl": 0.90,
      "b_deploy": 0.88
    }
  }
}
```

**For layer parameters:**
```json
// config/contextual_parametrization.json
{
  "layer_chain": {
    "discrete_mappings": {
      "hard_mismatch": 0.0,
      "all_contracts_pass": 1.0
    }
  }
}
```

### Step 2: Use CalibrationOrchestrator

```python
from farfan_pipeline.core.calibration.orchestrator import CalibrationOrchestrator

orchestrator = CalibrationOrchestrator.get_instance()
score = orchestrator.calibrate_method(
    method_id="method_001",
    context=calibration_context,
    is_executor=True
)
```

### Step 3: Convert YAML to JSON

```bash
# Convert YAML files
python -c "import yaml, json, sys; json.dump(yaml.safe_load(sys.stdin), sys.stdout, indent=2)" < config.yaml > config.json

# Update imports
# Change: import yaml
# To:     import json
```

### Step 4: Document Bayesian Priors

```json
// config/bayesian_priors.json
{
  "_metadata": {
    "description": "Bayesian prior distributions with justifications"
  },
  "evidence_strength": {
    "distribution": "beta",
    "alpha": 2.0,
    "beta": 5.0,
    "justification": "Weakly informative prior favoring lower evidence strength; based on pilot study showing 70% of initial evidence claims were weak"
  }
}
```

## Integration with CI/CD

Add to your pre-commit or CI pipeline:

```yaml
# .github/workflows/calibration-audit.yml
- name: Run Hardcoding Audit
  run: |
    python tools/hardcoding_audit_scanner.py
    if [ $? -ne 0 ]; then
      echo "Critical calibration hardcoding violations found!"
      exit 1
    fi
```

## Known Violator Files

The scanner specifically highlights these files as known violators:

1. **orchestrator.py** (lines 232-271)
   - Hardcoded layer computation scores
   - Direct numeric literals in `_compute_*_score()` methods

2. **layer_computers.py** (lines 141-156)
   - Hardcoded coefficients in `compute_unit_layer()`
   - Magic numbers in piecewise linear functions

These files require immediate refactoring to externalize all calibration values.

## Configuration

The scanner uses these default patterns:

```python
CALIBRATION_KEYWORDS = {
    'score', 'weight', 'threshold', 'coefficient',
    'alpha', 'beta', 'gamma',
    'b_theory', 'b_impl', 'b_deploy',
    'prior', 'posterior', 'likelihood',
    'calibration', 'layer', 'choquet'
}
```

To customize, modify `CalibrationHardcodingDetector.CALIBRATION_KEYWORDS` in the scanner source.

## Limitations

1. **False Positives**: May flag legitimate uses of calibration-named variables that aren't actual calibration values
2. **Dynamic Loading**: Cannot detect values loaded dynamically at runtime
3. **Obfuscation**: Cannot detect intentionally obfuscated hardcoding
4. **Comments**: Does not validate that priors are documented in comments

## Best Practices

1. **Run Regularly**: Include in CI/CD pipeline
2. **Fix Immediately**: Don't accumulate violations
3. **Document Rationale**: Always explain calibration values in config files
4. **Version Control**: Track all config file changes
5. **Review Carefully**: Manually review HIGH and CRITICAL violations

## Support

For questions or issues with the scanner:
1. Check `violations_audit.md` for detailed findings
2. Review this README for remediation steps
3. Consult CALIBRATION_ORCHESTRATOR_IMPLEMENTATION.md for architecture details

## License

Part of the FARFAN Mechanistic Policy Pipeline.
See main repository LICENSE file.
