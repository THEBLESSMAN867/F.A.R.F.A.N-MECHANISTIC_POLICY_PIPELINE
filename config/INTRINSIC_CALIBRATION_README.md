# Intrinsic Calibration System - @b-Only Single Source

## Overview
This directory contains the single source of truth for intrinsic calibration data with strict @b-only enforcement. The calibration system provides baseline quality scores for 128 methods across the F.A.R.F.A.N pipeline.

## Files
- `intrinsic_calibration.json` - Main calibration data file (DO NOT EDIT MANUALLY)
- `intrinsic_calibration_rubric.json` - Scoring rubric for calibration computation

## Structure
The calibration file contains:
```json
{
  "_metadata": {
    "version": "1.0.0",
    "total_methods": 128,
    "computed_methods": 108,
    "coverage_percent": 84.4
  },
  "ClassName.method_name": {
    "intrinsic_score": [low, high],
    "b_theory": float,
    "b_impl": float,
    "b_deploy": float,
    "calibration_status": "computed|pending|excluded|none",
    "layer": "engine|processor|utility",
    "last_updated": "ISO8601"
  }
}
```

## @b-Layer Scores
Each method has three @b-layer scores:
- **b_theory**: Theoretical soundness (0-1)
- **b_impl**: Implementation quality (0-1)
- **b_deploy**: Deployment readiness (0-1)

## Calibration Status
- **computed**: Actual @b values from calibration process
- **pending**: Fallback to @b=0.5 (neutral baseline)
- **excluded**: Method skipped (returns None)
- **none**: Fallback to @b=0.3 with warning (low confidence)

## Usage
```python
from farfan_pipeline.core.calibration.intrinsic_calibration_loader import (
    get_method_calibration
)

# Get calibration for a method
cal = get_method_calibration("ClassName.method_name")
if cal is not None:  # Not excluded
    composite_b = cal.get_composite_b()
    print(f"Method @b score: {composite_b:.2f}")
```

## Validation
Run validation tests:
```bash
pytest tests/test_intrinsic_purity.py -v
pytest tests/test_intrinsic_pipeline_behavior.py -v
```

## Purity Enforcement
The system enforces strict @b-only data:
- ✓ NO @chain, @q, @d, @p, @C, @u, @m keys
- ✓ NO final_score or layer_scores
- ✓ ONLY intrinsic_score, b_theory, b_impl, b_deploy, calibration_status, layer, last_updated

## Requirements
- ✓ Coverage >= 80% (currently 84.4%)
- ✓ At least 30 computed methods (currently 108)
- ✓ No contamination from other calibration layers

## Current Statistics
- Total methods: 128
- Computed: 108 (84.4%)
- Excluded: 20 (15.6%)
- Coverage: PASS (>=80%)
- Minimum executors: PASS (>=30)

## Fallback Behavior
| Status | b_theory | b_impl | b_deploy | Action |
|--------|----------|--------|----------|--------|
| computed | actual | actual | actual | Use calibrated values |
| pending | 0.5 | 0.5 | 0.5 | Neutral baseline |
| excluded | N/A | N/A | N/A | Skip method execution |
| none | 0.3 | 0.3 | 0.3 | Low confidence + warning |

## Error Handling
The loader will raise `ValueError` with message "Intrinsic calibration incomplete or contaminated" if:
- Coverage < 80%
- Contaminated keys detected
- File not found or invalid JSON

## Regeneration
To regenerate calibration data:
```bash
python scripts/gen_cal_standalone.py
```

## Integration
The intrinsic calibration loader is integrated into the pipeline orchestrator and provides @b scores for all 128 methods. The loader implements a singleton pattern and verifies data purity on initialization.
