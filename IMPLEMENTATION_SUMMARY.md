# Implementation Summary: _construct_task Method

## Overview
Implemented the `_construct_task` method in `src/farfan_pipeline/core/orchestrator/task_planner.py` with comprehensive validation logic and a new signature accepting routing results, patterns, signals, and correlation tracking.

## Changes Made

### 1. Added ChunkRoutingResult Type
**File:** `src/farfan_pipeline/core/orchestrator/task_planner.py`

```python
@dataclass(frozen=True, slots=True)
class ChunkRoutingResult:
    policy_area_id: str
    chunk_id: str
```

### 2. Implemented New _construct_task Method
**Signature:**
```python
def _construct_task(
    question: dict[str, Any],
    routing_result: ChunkRoutingResult,
    applicable_patterns: tuple[Any, ...],
    resolved_signals: tuple[Any, ...],
    generated_task_ids: set[str],
    correlation_id: str,
) -> ExecutableTask
```

**Validation Logic:**

1. **Extract question_global field**
   - Uses `question.get('question_global')`
   - Defaults question_id to 'UNKNOWN' if missing

2. **Validate question_global is not None**
   - Raises `ValueError` with message: 
     `"Task construction failure for {question_id}: question_global field missing or None"`

3. **Validate question_global is an integer**
   - Uses `isinstance(question_global, int)` check
   - Raises `ValueError` with message:
     `"Task construction failure for {question_id}: question_global must be an integer, got {type_name}"`

4. **Validate question_global range (0-999)**
   - Checks `0 <= question_global <= 999`
   - Raises `ValueError` with message:
     `"Task construction failure for {question_id}: question_global must be in range 0-999, got {value}"`

5. **Construct task_id**
   - Format: `f"MQC-{question_global:03d}_{routing_result.policy_area_id}"`
   - Uses leading zeros for formatting (e.g., MQC-001, MQC-042, MQC-999)

6. **Check for duplicate task_id**
   - Checks if task_id exists in `generated_task_ids` set
   - Raises `ValueError` with message: `"Duplicate task_id detected: {task_id}"`

7. **Reserve task_id immediately**
   - Adds task_id to `generated_task_ids` set BEFORE continuing construction
   - Ensures ID is reserved even if subsequent construction steps fail

8. **Complete task construction**
   - Creates MicroQuestionContext with routing_result data
   - Creates ExecutableTask with all validated fields
   - Stores correlation_id in task metadata

### 3. Preserved Legacy Function
Renamed the original `_construct_task` to `_construct_task_legacy` to maintain backward compatibility with existing tests.

### 4. Updated Tests
**File:** `tests/core/test_task_planner.py`

- Updated imports to include both `_construct_task` and `_construct_task_legacy`
- Updated existing tests to use `_construct_task_legacy`
- Added comprehensive test class `TestConstructTaskNew` with 8 test scenarios:
  1. Valid inputs test
  2. Missing question_global test
  3. Missing question_global with UNKNOWN id test
  4. Invalid type for question_global test
  5. Below range test (negative value)
  6. Above range test (value > 999)
  7. Duplicate task_id test
  8. Boundary values test (0 and 999)
  9. Task ID formatting test (leading zeros)

## Key Features

### Error Messages
All error messages follow the pattern:
- Include the question_id (or "UNKNOWN" if missing)
- Clearly describe the validation failure
- Include the actual problematic value where applicable

### Task ID Reservation
The implementation ensures task_id is added to `generated_task_ids` immediately after duplicate check and before any further processing. This prevents:
- Race conditions in concurrent scenarios
- Partial construction leaving IDs unreserved
- Duplicate ID generation if construction fails partway through

### Type Safety
- Uses proper type hints for all parameters
- Validates types at runtime before proceeding
- Uses frozen dataclass for ChunkRoutingResult

### Data Flow
1. Extract and validate question_global
2. Construct and validate task_id
3. Reserve task_id in set
4. Transform patterns tuple to list
5. Transform signals tuple to dict
6. Create frozen MicroQuestionContext
7. Create mutable ExecutableTask
8. Return completed task

## Files Modified
1. `src/farfan_pipeline/core/orchestrator/task_planner.py` - Core implementation
2. `tests/core/test_task_planner.py` - Test updates
3. `verify_construct_task.py` - Verification script (new file)
4. `IMPLEMENTATION_SUMMARY.md` - This documentation (new file)

## Testing
The implementation includes:
- 8 comprehensive test cases covering all validation scenarios
- Boundary value testing (0, 999)
- Error message verification
- Task ID formatting verification
- Duplicate detection verification
