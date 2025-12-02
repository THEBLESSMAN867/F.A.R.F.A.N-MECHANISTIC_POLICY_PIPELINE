"""
Port interface for recommendation engine.

Defines the abstract interface for recommendation generation, following
the Ports and Adapters (Hexagonal) architecture pattern.

Version: 1.0.0
"""

from typing import Any, Protocol


class RecommendationEnginePort(Protocol):
    """Port for recommendation engine operations.

    Provides abstract interface for multi-level recommendation generation.
    Core orchestrator depends on this port, not the concrete implementation.

    Implementations must support three levels of recommendations:
    - MICRO: Question-level recommendations (PA-DIM combinations)
    - MESO: Cluster-level recommendations (CL01-CL04)
    - MACRO: Plan-level strategic recommendations
    """

    def generate_all_recommendations(
        self,
        micro_scores: dict[str, float],
        cluster_data: dict[str, Any],
        macro_data: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate recommendations at all three levels.

        Args:
            micro_scores: Dictionary mapping "PA##-DIM##" to scores (0.0-3.0)
            cluster_data: Dictionary with cluster metrics:
                {
                    'CL01': {'score': 75.0, 'variance': 0.15, 'weak_pa': 'PA02'},
                    'CL02': {'score': 62.0, 'variance': 0.22, 'weak_pa': 'PA05'},
                    ...
                }
            macro_data: Dictionary with macro-level metrics:
                {
                    'macro_score': 68.5,
                    'cross_cutting_coherence': 0.72,
                    'systemic_gaps': ['gap1', 'gap2'],
                    'strategic_alignment': 0.65
                }
            context: Optional context for template rendering

        Returns:
            Dictionary mapping level to RecommendationSet:
            {
                'MICRO': RecommendationSet(...),
                'MESO': RecommendationSet(...),
                'MACRO': RecommendationSet(...)
            }

        Requires:
            - micro_scores keys follow "PA##-DIM##" format
            - cluster_data keys follow "CL##" format
            - macro_data contains required metrics

        Ensures:
            - Returns dict with 'MICRO', 'MESO', 'MACRO' keys
            - Each value is a RecommendationSet with to_dict() method
            - Generated_at timestamp is present
        """
        ...

    def generate_micro_recommendations(
        self, scores: dict[str, float], context: dict[str, Any] | None = None
    ) -> Any:
        """Generate MICRO-level recommendations.

        Args:
            scores: Dictionary mapping "PA##-DIM##" to scores (0.0-3.0)
            context: Optional context for template rendering

        Returns:
            RecommendationSet with MICRO recommendations

        Requires:
            - scores keys follow "PA##-DIM##" format

        Ensures:
            - Returns RecommendationSet with level='MICRO'
            - Contains list of matched recommendations
        """
        ...

    def generate_meso_recommendations(
        self, cluster_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> Any:
        """Generate MESO-level recommendations.

        Args:
            cluster_data: Dictionary with cluster metrics
            context: Optional context for template rendering

        Returns:
            RecommendationSet with MESO recommendations

        Requires:
            - cluster_data keys follow "CL##" format
            - Each cluster has score, variance, weak_pa fields

        Ensures:
            - Returns RecommendationSet with level='MESO'
            - Contains list of matched recommendations
        """
        ...

    def generate_macro_recommendations(
        self, macro_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> Any:
        """Generate MACRO-level recommendations.

        Args:
            macro_data: Dictionary with macro-level metrics
            context: Optional context for template rendering

        Returns:
            RecommendationSet with MACRO recommendations

        Requires:
            - macro_data contains macro_score
            - macro_data contains strategic metrics

        Ensures:
            - Returns RecommendationSet with level='MACRO'
            - Contains list of matched recommendations
        """
        ...

    def reload_rules(self) -> None:
        """Reload recommendation rules from disk.

        Enables hot-reloading of rules during development/operation.

        Ensures:
            - Rules are revalidated against schema
            - Engine state is consistent after reload
        """
        ...


__all__ = ["RecommendationEnginePort"]
