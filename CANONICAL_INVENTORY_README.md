# Canonical Method Inventory

## Overview

This directory contains three JSON files that provide a comprehensive inventory of all methods in the `src/farfan_pipeline/` codebase:

1. **canonical_method_inventory.json** - Complete method catalog with signatures
2. **method_statistics.json** - Statistical analysis by role, module, and executors
3. **excluded_methods.json** - Methods flagged as 'never calibrate'

## Files

### 1. canonical_method_inventory.json

**Structure:**
```json
{
  "methods": {
    "<canonical_id>": {
      "canonical_name": "module.Class.method",
      "file_path": "relative/path/to/file.py",
      "line_number": 123,
      "class_name": "ClassName" | null,
      "role": "executor|analyzer|processor|...",
      "is_executor": true|false,
      "signature": {
        "parameters": [
          {
            "name": "param_name",
            "kind": "POSITIONAL_OR_KEYWORD|VAR_POSITIONAL|...",
            "type_hint": "type annotation" | null,
            "has_default": true|false,
            "default_repr": "default value" | null
          }
        ]
      }
    }
  },
  "metadata": {
    "total_methods": 2774,
    "scan_timestamp": "ISO 8601 timestamp",
    "source_directory": "src/farfan_pipeline"
  }
}
```

**Total Methods:** 2,773  
**File Size:** ~2.3 MB

### 2. method_statistics.json

**Structure:**
```json
{
  "total_methods": 2774,
  "total_executors": 192,
  "by_role": {
    "executor": 208,
    "analyzer": 271,
    "processor": 82,
    "scorer": 160,
    "orchestrator": 110,
    "extractor": 157,
    "ingestor": 114,
    "core": 1326,
    "utility": 346
  },
  "by_module": {
    "core": 1078,
    "analysis": 631,
    "processing": 405,
    "utils": 241,
    ...
  },
  "executor_distribution": {
    "core": 185,
    "observability": 2,
    "optimization": 1,
    "patterns": 2,
    "utils": 2
  }
}
```

**File Size:** ~800 bytes

### 3. excluded_methods.json

**Structure:**
```json
{
  "excluded_methods": [
    {
      "canonical_id": "module.Class.method",
      "reason": "trivial_formatter|utility_formatter",
      "method_name": "__init__",
      "file_path": "path/to/file.py",
      "line_number": 123
    }
  ],
  "exclusion_reason": "never calibrate",
  "total_excluded": 304
}
```

**Total Excluded:** 304 methods  
**File Size:** ~72 KB

## Role Classification

Methods are classified into the following roles:

- **executor** - Executor pattern implementations (192 total)
- **analyzer** - Analysis and inference operations (271 total)
- **processor** - Data transformation and processing (82 total)
- **scorer** - Scoring and evaluation methods (160 total)
- **orchestrator** - Workflow orchestration (110 total)
- **extractor** - Feature and information extraction (157 total)
- **ingestor** - Data ingestion and parsing (114 total)
- **core** - Core framework methods (1,326 total)
- **utility** - Helper and utility functions (346 total)

## Exclusion Criteria

Methods are excluded from calibration if they meet any of these criteria:

1. **Trivial Formatters:**
   - `__init__`, `__str__`, `__repr__`, `__del__`, `__format__`
   - `__eq__`, `__ne__`, `__hash__`, `__lt__`, `__le__`, `__gt__`, `__ge__`
   - `to_string`, `to_json`, `to_dict`, `from_dict`

2. **Utility Formatters:**
   - Methods with role="utility" and containing:
     - `_format`, `_helper`, `_to_`, `_from_`

## Generation

To regenerate the inventory files:

```bash
python generate_canonical_inventory.py
```

To verify the generated files:

```bash
python verify_canonical_inventory.py
```

## Use Cases

1. **Calibration Planning** - Identify which methods require calibration
2. **Executor Analysis** - Track all executor pattern implementations
3. **Code Coverage** - Ensure comprehensive method inventory
4. **Architecture Analysis** - Understand method distribution across modules
5. **Refactoring Support** - Identify dependencies and relationships

## Version Information

- **Generated:** 2025-12-03
- **Python Version:** 3.12+
- **Source Directory:** `src/farfan_pipeline/`
- **Total Files Scanned:** All Python files in source directory

## Notes

- Canonical identifiers use dot notation: `module.Class.method`
- Line numbers indicate the start of method definitions
- Type hints are preserved from source code annotations
- Default parameter values are represented as strings
- Async methods are included with standard function definitions
