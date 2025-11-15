"""
Scoring Module

Implements TYPE_A through TYPE_F scoring modalities with strict validation
and reproducible results.
"""

# Import from parent module (saaaaaa.analysis.scoring) for Evidence and MicroQuestionScorer
# These exist in the module file, not the package's scoring.py
from saaaaaa.analysis.scoring import Evidence, MicroQuestionScorer

# Import from package's scoring.py for the rest
from .scoring import (
    EvidenceStructureError,
    ModalityConfig,
    ModalityValidationError,
    QualityLevel,
    ScoredResult,
    ScoringError,
    ScoringModality,
    ScoringValidator,
    apply_scoring,
    determine_quality_level,
)

__all__ = [
    "Evidence",
    "EvidenceStructureError",
    "MicroQuestionScorer",
    "ModalityConfig",
    "ModalityValidationError",
    "QualityLevel",
    "ScoredResult",
    "ScoringError",
    "ScoringModality",
    "ScoringValidator",
    "apply_scoring",
    "determine_quality_level",
]
