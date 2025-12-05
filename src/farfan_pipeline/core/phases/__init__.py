"""
Canonical Phase Implementations - F.A.R.F.A.N Pipeline
======================================================

This package contains the canonical implementations of all pipeline phases:

Phase 0: Input Validation (Raw input → Validated CanonicalInput)
Phase 1: SPC Ingestion (CanonicalInput → CanonPolicyPackage)
Phase 2: Micro Questions (PreprocessedDocument → Phase2Result)
Phase 6: Schema Validation (Raw data → Validated schemas)
Phase 7: Task Construction (Validated schemas → ExecutableTask set)
Phase 8: Execution Plan Assembly (ExecutableTask set → ExecutionPlan)

All phases follow the PhaseContract protocol with:
- Explicit input/output contracts
- Mandatory field validation
- Error propagation semantics
- Deterministic execution
- Provenance tracking
"""

from src.farfan_pipeline.core.phases.phase6_schema_validation import (
    Phase6SchemaValidationOutput,
    ValidatedChunkSchema,
    ValidatedQuestionSchema,
    phase6_schema_validation,
)
from src.farfan_pipeline.core.phases.phase7_task_construction import (
    Phase7TaskConstructionOutput,
    phase7_task_construction,
)
from src.farfan_pipeline.core.phases.phase8_execution_plan import (
    ExecutionPlan,
    Phase8ExecutionPlanOutput,
    phase8_execution_plan_assembly,
)

__all__ = [
    "Phase6SchemaValidationOutput",
    "ValidatedQuestionSchema",
    "ValidatedChunkSchema",
    "phase6_schema_validation",
    "Phase7TaskConstructionOutput",
    "phase7_task_construction",
    "ExecutionPlan",
    "Phase8ExecutionPlanOutput",
    "phase8_execution_plan_assembly",
]
