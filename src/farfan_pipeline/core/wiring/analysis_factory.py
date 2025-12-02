"""
Analysis Module Factory for Dependency Injection.

Provides concrete implementations of analysis ports without creating
direct dependencies between orchestrator → processing → analysis layers.

This factory uses lazy imports to break the circular dependency chain:
- Ports are defined in core layer (no dependencies)
- Factory is in core/wiring (can import from analysis)
- Processing layer depends only on ports (not analysis)
- Factory injects implementations at runtime

Architecture:
    core/ports.py → Define abstract protocols
    core/wiring/analysis_factory.py → Lazy import concrete implementations
    processing/policy_processor.py → Accept ports via dependency injection
"""

from typing import Any, Protocol


def create_document_loader() -> Any:
    """Create document loader implementation.

    Returns:
        Implementation of PortDocumentLoader
    """
    from farfan_pipeline.analysis.Analyzer_one import DocumentProcessor
    return DocumentProcessor


def create_municipal_ontology() -> Any:
    """Create municipal ontology implementation.

    Returns:
        Instance implementing PortMunicipalOntology
    """
    from farfan_pipeline.analysis.Analyzer_one import MunicipalOntology
    return MunicipalOntology()


def create_semantic_analyzer(ontology: Any | None = None) -> Any:
    """Create semantic analyzer implementation.

    Args:
        ontology: Optional ontology instance (creates new if None)

    Returns:
        Instance implementing PortSemanticAnalyzer
    """
    from farfan_pipeline.analysis.Analyzer_one import SemanticAnalyzer, MunicipalOntology
    if ontology is None:
        ontology = MunicipalOntology()
    return SemanticAnalyzer(ontology)


def create_performance_analyzer(ontology: Any | None = None) -> Any:
    """Create performance analyzer implementation.

    Args:
        ontology: Optional ontology instance (creates new if None)

    Returns:
        Instance implementing PortPerformanceAnalyzer
    """
    from farfan_pipeline.analysis.Analyzer_one import PerformanceAnalyzer, MunicipalOntology
    if ontology is None:
        ontology = MunicipalOntology()
    return PerformanceAnalyzer(ontology)


def create_contradiction_detector() -> Any:
    """Create contradiction detector implementation.

    Returns:
        Instance implementing PortContradictionDetector

    Note:
        Falls back to lightweight implementation if module unavailable
    """
    try:
        from farfan_pipeline.analysis.contradiction_deteccion import PolicyContradictionDetector
        return PolicyContradictionDetector()
    except Exception:
        from farfan_pipeline.processing.policy_processor import _FallbackContradictionDetector
        return _FallbackContradictionDetector()


def create_temporal_logic_verifier() -> Any:
    """Create temporal logic verifier implementation.

    Returns:
        Instance implementing PortTemporalLogicVerifier

    Note:
        Falls back to lightweight implementation if module unavailable
    """
    try:
        from farfan_pipeline.analysis.contradiction_deteccion import TemporalLogicVerifier
        return TemporalLogicVerifier()
    except Exception:
        from farfan_pipeline.processing.policy_processor import _FallbackTemporalVerifier
        return _FallbackTemporalVerifier()


def create_bayesian_confidence_calculator() -> Any:
    """Create Bayesian confidence calculator implementation.

    Returns:
        Instance implementing PortBayesianConfidenceCalculator

    Note:
        Falls back to lightweight implementation if module unavailable
    """
    try:
        from farfan_pipeline.analysis.contradiction_deteccion import BayesianConfidenceCalculator
        return BayesianConfidenceCalculator()
    except Exception:
        from farfan_pipeline.processing.policy_processor import _FallbackBayesianCalculator
        return _FallbackBayesianCalculator()


def create_municipal_analyzer() -> Any:
    """Create municipal analyzer implementation.

    Returns:
        Instance implementing PortMunicipalAnalyzer
    """
    from farfan_pipeline.analysis.Analyzer_one import MunicipalAnalyzer
    return MunicipalAnalyzer()


def create_analysis_components() -> dict[str, Any]:
    """Create all analysis components with shared ontology.

    Returns:
        Dictionary containing all initialized analysis components:
        - document_loader: DocumentProcessor class (not instance)
        - ontology: MunicipalOntology instance
        - semantic_analyzer: SemanticAnalyzer instance
        - performance_analyzer: PerformanceAnalyzer instance
        - contradiction_detector: PolicyContradictionDetector instance
        - temporal_verifier: TemporalLogicVerifier instance
        - confidence_calculator: BayesianConfidenceCalculator instance
        - municipal_analyzer: MunicipalAnalyzer instance
    """
    ontology = create_municipal_ontology()

    return {
        'document_loader': create_document_loader(),
        'ontology': ontology,
        'semantic_analyzer': create_semantic_analyzer(ontology),
        'performance_analyzer': create_performance_analyzer(ontology),
        'contradiction_detector': create_contradiction_detector(),
        'temporal_verifier': create_temporal_logic_verifier(),
        'confidence_calculator': create_bayesian_confidence_calculator(),
        'municipal_analyzer': create_municipal_analyzer(),
    }


__all__ = [
    'create_document_loader',
    'create_municipal_ontology',
    'create_semantic_analyzer',
    'create_performance_analyzer',
    'create_contradiction_detector',
    'create_temporal_logic_verifier',
    'create_bayesian_confidence_calculator',
    'create_municipal_analyzer',
    'create_analysis_components',
]
