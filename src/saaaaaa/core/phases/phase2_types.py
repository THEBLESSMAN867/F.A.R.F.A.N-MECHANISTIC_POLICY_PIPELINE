"""
Types for Phase 2 (Microquestions)
==================================

This module defines the canonical data structures for the output of
Phase 2, which involves processing the PreprocessedDocument to generate
a series of microquestions and their answers.

These types are used by the PhaseOrchestrator to validate and record
the results of the core orchestrator's execution.

Author: F.A.R.F.A.N Architecture Team
Date: 2025-11-21
"""

from __future__ import annotations

from typing import Any, TypedDict, List


class Phase2QuestionResult(TypedDict):
    """
    Represents the result for a single microquestion generated
    and answered during Phase 2.
    """
    base_slot: str
    question_id: str
    question_global: int | None
    policy_area_id: str | None
    dimension_id: str | None
    cluster_id: str | None
    evidence: dict[str, Any]
    validation: dict[str, Any]
    trace: dict[str, Any]


class Phase2Result(TypedDict):
    """
    Represents the complete output of Phase 2, containing all
    the generated microquestions.
    """
    questions: List[Phase2QuestionResult]
