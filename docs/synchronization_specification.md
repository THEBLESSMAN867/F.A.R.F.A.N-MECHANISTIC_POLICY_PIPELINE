# Irrigation Synchronization Specification

## Overview

The Irrigation Synchronization system coordinates the mapping of questionnaire questions to document chunks, generating a deterministic execution plan for the F.A.R.F.A.N policy analysis pipeline.

## Architecture

### Core Components

1. **IrrigationSynchronizer**: Main orchestrator that coordinates chunk→question→task→plan flow
2. **ExecutionPlan**: Immutable execution plan with cryptographic integrity verification
3. **Task**: Single unit of work representing one question applied to one chunk in a policy area

### Data Flow

```
questionnaire_monolith.json → Questions (300)
                             ↓
document_chunks (60)      →  Tasks (300 × 10 × 60 = 180,000)
                             ↓
                          ExecutionPlan
                             ↓
                          Orchestrator Phase 2+
```

## Synchronization Process

### Phase 0: Initialization

```python
synchronizer = IrrigationSynchronizer(
    questionnaire=questionnaire_data,
    document_chunks=document_chunks
)
```

**Actions:**
- Generate UUID4 correlation_id
- Count questions across all dimensions (D1-D6)
- Count document chunks
- Emit structured JSON log with correlation_id

**Observability:**
```json
{
  "event": "irrigation_synchronizer_init",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question_count": 300,
  "chunk_count": 60,
  "timestamp": 1701234567.89
}
```

### Phase 1: Question Extraction

**Process:**
1. Parse questionnaire blocks (D1-D6)
2. Extract questions in deterministic order:
   - D1_Q01, D1_Q02, ..., D1_Q50
   - D2_Q01, D2_Q02, ..., D2_Q50
   - ...
   - D6_Q01, D6_Q02, ..., D6_Q50
3. Capture question metadata (text, patterns, dimension)

### Phase 2: Task Generation

**Formula:**
```
tasks = questions × policy_areas × chunks
      = 300 × 10 × 60
      = 180,000 tasks
```

**Task Structure:**
```python
@dataclass(frozen=True)
class Task:
    task_id: str              # "D1_Q01_PA01_chunk_0000"
    dimension: str            # "D1"
    question_id: str          # "D1_Q01"
    policy_area: str          # "PA01"
    chunk_id: str             # "chunk_0000"
    chunk_index: int          # 0
    question_text: str        # "¿Se identifican problemas...?"
```

**Generation Logic:**
```python
for question in questions:
    for policy_area in ['PA01', 'PA02', ..., 'PA10']:
        for chunk_idx, chunk in enumerate(chunks):
            task = Task(
                task_id=f"{question.id}_{policy_area}_{chunk.id}",
                dimension=question.dimension,
                question_id=question.id,
                policy_area=policy_area,
                chunk_id=chunk.id,
                chunk_index=chunk_idx,
                question_text=question.text
            )
```

### Phase 3: Integrity Hashing

**Algorithm:**
1. Serialize tasks to canonical JSON (sorted keys)
2. Compute Blake3 hash (or SHA256 fallback)
3. Generate plan_id from hash prefix

**Code:**
```python
task_data = json.dumps(
    [{"task_id": t.task_id, "dimension": t.dimension, ...} for t in tasks],
    sort_keys=True
).encode('utf-8')

integrity_hash = blake3.blake3(task_data).hexdigest()
plan_id = f"plan_{integrity_hash[:16]}"
```

### Phase 4: Plan Assembly

**ExecutionPlan Structure:**
```python
@dataclass(frozen=True)
class ExecutionPlan:
    plan_id: str              # "plan_a1b2c3d4e5f67890"
    tasks: tuple[Task, ...]   # (task1, task2, ..., task180000)
    chunk_count: int          # 60
    question_count: int       # 300
    integrity_hash: str       # Full Blake3/SHA256 hash
    created_at: str           # ISO 8601 timestamp
    correlation_id: str       # UUID4 from initialization
```

## Integration with Orchestrator

### Invocation Point

The synchronizer is called **after Phase 1** (SPC Ingestion) completes:

```python
# In Orchestrator.process_development_plan_async()
if phase_id == 1 and success and not aborted:
    document = self._context.get('document')
    chunks = getattr(document, 'chunks', [])
    
    synchronizer = IrrigationSynchronizer(
        questionnaire=self._monolith_data,
        document_chunks=chunks
    )
    
    self._execution_plan = synchronizer.build_execution_plan()
```

### Error Handling

**ValueError on Empty Data:**
```python
try:
    plan = synchronizer.build_execution_plan()
except ValueError as e:
    logger.error(f"Synchronization failed: {e}")
    self.request_abort(f"Cannot proceed without execution plan: {e}")
    raise
```

**Abort Behavior:**
- Pipeline aborts with non-zero exit code
- Error logged in verification_manifest.json
- Correlation_id propagates to all error logs

## Observability

### Structured Logging

All log entries use JSON format with correlation_id:

```json
{
  "event": "build_execution_plan_start",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question_count": 300,
  "chunk_count": 60,
  "phase": "synchronization_phase_0"
}
```

### Prometheus Metrics

**synchronization_duration_seconds (Histogram):**
- Tracks time to build execution plan
- Buckets: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

**tasks_constructed_total (Counter):**
- Labels: dimension, policy_area
- Incremented for each task created

**synchronization_failures_total (Counter):**
- Labels: error_type
- Tracks failure reasons (empty_chunks, empty_questions, ValueError, etc.)

### Correlation ID Propagation

The correlation_id flows through all 10 phases:

```
Phase 0 (Config)        → correlation_id in logs
Phase 1 (SPC Ingestion) → correlation_id in logs
Synchronization         → correlation_id in logs ✓
Phase 2 (Questions)     → correlation_id in logs
...
Phase 10 (Export)       → correlation_id in logs
```

## Verification Manifest Integration

### Synchronization Section

Added to `verification_manifest.json`:

```json
{
  "synchronization": {
    "plan_id": "plan_a1b2c3d4e5f67890",
    "integrity_hash": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890",
    "task_count": 180000,
    "chunk_count": 60,
    "question_count": 300,
    "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "created_at": "2024-12-03T10:30:00Z"
  }
}
```

### CI Assertions

GitHub Actions workflow verifies:

1. **Manifest structure:** `synchronization` section exists
2. **Task count:** Exactly 180,000 tasks (300 q × 10 pa × 60 chunks)
3. **Integrity hash:** Can be recomputed and matches original

```yaml
- name: Verify synchronization manifest
  run: |
    python -c "
    import json
    manifest = json.load(open('artifacts/verification_manifest.json'))
    assert manifest['synchronization']['task_count'] == 180000
    assert len(manifest['synchronization']['integrity_hash']) == 64
    "
```

## Determinism Guarantees

### Sources of Determinism

1. **Question ordering:** Fixed (D1_Q01 → D6_Q50)
2. **Policy area ordering:** Fixed (PA01 → PA10)
3. **Chunk ordering:** Preserved from Phase 1
4. **Task ID generation:** Formula-based (no randomness)
5. **Hash algorithm:** Blake3 (deterministic)

### Reproducibility

Given identical inputs:
- Same questionnaire
- Same chunks (order + content)

The system ALWAYS produces:
- Same plan_id
- Same integrity_hash
- Same task ordering

## Performance Characteristics

### Time Complexity

- Question extraction: O(Q) where Q = question count
- Task generation: O(Q × PA × C) where PA = policy areas, C = chunks
- Hash computation: O(T) where T = task count
- **Overall:** O(Q × PA × C)

### Space Complexity

- Tasks: O(Q × PA × C) = O(180,000) tasks
- Each task: ~200 bytes
- **Total:** ~36 MB for execution plan

### Benchmarks

On typical hardware:
- Question extraction: < 100ms
- Task generation: < 500ms
- Hash computation: < 200ms
- **Total synchronization:** < 1 second

## Error Scenarios

### Empty Chunks

**Trigger:** Phase 1 produces no chunks

**Behavior:**
```python
ValueError: No document chunks provided
```

**Mitigation:** Abort pipeline, log error with correlation_id

### Empty Questionnaire

**Trigger:** No questions found in questionnaire

**Behavior:**
```python
ValueError: No questions found in questionnaire
```

**Mitigation:** Abort pipeline, validate questionnaire before pipeline start

### Hash Verification Failure

**Trigger:** Recomputed hash doesn't match original

**Behavior:** CI test fails, manifest marked invalid

**Mitigation:** Investigate non-deterministic task generation

## Testing Strategy

### Unit Tests

1. Synchronizer initialization
2. Question extraction logic
3. Task generation algorithm
4. Integrity hash computation
5. Correlation ID uniqueness

### Integration Tests

1. End-to-end with real questionnaire
2. 60-chunk document processing
3. Plan determinism verification
4. Logging correlation_id propagation
5. Prometheus metrics recording

### CI Tests

1. Manifest structure validation
2. Task count assertion (180,000)
3. Integrity hash recomputation
4. Correlation ID consistency across logs

## Future Enhancements

1. **Parallel Task Generation:** Distribute across workers
2. **Streaming Task Processing:** Avoid loading all 180K tasks in memory
3. **Incremental Hashing:** Update hash as tasks are generated
4. **Task Prioritization:** Sort by chunk relevance score
5. **Dynamic Policy Area Filtering:** Skip irrelevant areas per chunk

## References

- [SIGNAL_IRRIGATION_ARCHITECTURE_AUDIT.md](../SIGNAL_IRRIGATION_ARCHITECTURE_AUDIT.md)
- [Orchestrator Core Implementation](../src/farfan_pipeline/core/orchestrator/core.py)
- [Questionnaire Monolith Schema](../system/config/questionnaire/questionnaire_monolith.json)
