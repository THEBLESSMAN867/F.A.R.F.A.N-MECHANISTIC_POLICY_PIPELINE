# Canonical Method Inventory Verification

This directory contains the canonical method inventory, verification scripts, and scanning tools for the F.A.R.F.A.N policy analysis pipeline.

## Files

- `canonical_method_inventory.json` - The canonical inventory of all methods in the pipeline
- `verify_inventory.py` - Verification script to validate the inventory against required criteria
- `scan_methods_inventory.py` - Script to scan source code and extract method signatures

## Usage

### Verify Canonical Method Inventory

To verify the canonical method inventory:

```bash
python scripts/inventory/verify_inventory.py
```

The script will exit with code 0 if all checks pass, or code 1 if any check fails.

### Scan Source Code for Methods

To scan the source code and extract all methods:

```bash
python scripts/inventory/scan_methods_inventory.py > inventory.json
```

## Verification Criteria

The verification script checks:

1. **Total methods ≥ 1995** - Ensures the inventory contains at least 1995 methods
2. **All 30 D1Q1-D6Q5 executors present** - Validates that all 30 dimension-question executors are present with `is_executor=true`
3. **No duplicate canonical IDs** - Ensures there are no duplicate canonical identifiers
4. **Every method has non-empty role** - Validates that every method has a non-empty role field

## Canonical Inventory Structure

The `canonical_method_inventory.json` file should have the following structure:

```json
{
  "metadata": {
    "scan_timestamp": "ISO 8601 timestamp",
    "repository": "Repository name",
    "total_methods": 2000,
    "description": "Description"
  },
  "methods": {
    "method_id": {
      "method_id": "unique identifier",
      "canonical_name": "ClassName.method_name",
      "class_name": "ClassName",
      "is_executor": true/false,
      "role": "EXECUTOR|UTILITY|ANALYZER|..."
    }
  }
}
```

## Executor Naming Convention

Executors must follow the D{n}Q{m} naming pattern where:
- n = dimension (1-6)
- m = question (1-5)

Examples: D1Q1, D1Q2, ..., D6Q5 (30 total executors)

The verification script will match executors using various patterns:
- `D1Q1`
- `D1_Q1`
- `D1-Q1`
- `D1_Q_1`

## Method Scanner Output Format

The `scan_methods_inventory.py` script outputs JSON with the following structure:

```json
{
  "metadata": {
    "total_methods": 2774,
    "source_directory": "src/farfan_pipeline"
  },
  "methods": [
    {
      "module_path": "farfan_pipeline.analysis.factory",
      "class_name": null,
      "method_name": "load_json",
      "signature": [
        {
          "name": "file_path",
          "kind": "positional_or_keyword",
          "default": null,
          "type_hint": "str | Path"
        }
      ],
      "line_number": 52,
      "canonical_id": "farfan_pipeline.analysis.factory.load_json",
      "file_path": "src/farfan_pipeline/analysis/factory.py"
    }
  ]
}
```

### Captured Information

For each method/function:
- **module_path**: Dot-separated module path (e.g., `farfan_pipeline.core.orchestrator.core`)
- **class_name**: Class name if method is in a class, else `null`
- **method_name**: Function/method name
- **signature**: List of parameters with:
  - `name`: Parameter name
  - `kind`: Parameter kind (`positional_or_keyword`, `positional_only`, `keyword_only`, `var_positional`, `var_keyword`)
  - `default`: Default value as string, or `null`
  - `type_hint`: Type annotation as string, or `null`
- **line_number**: Starting line number in source file
- **canonical_id**: Full identifier in format `module.Class.method` or `module.function`
- **file_path**: Relative path from repo root

### Scanner Features

- ✅ Captures top-level functions and class methods
- ✅ Excludes nested inner functions
- ✅ Handles async functions (`async def`)
- ✅ Captures all parameter types (positional, keyword-only, *args, **kwargs)
- ✅ Preserves type hints and default values
- ✅ Reports syntax errors and continues processing
