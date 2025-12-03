"""
Choquet Integral Adapter for Processing Aggregation

This module adapts the calibration ChoquetAggregator for use in processing-level
score aggregation. It handles the impedance mismatch between:
- Calibration layer scores (8 layers: @b, @chain, @q, @d, @p, @C, @u, @m)
- Processing dimension/area scores (numeric scores with weights)

Key adaptations:
- Maps dimension/question indices to pseudo-layer IDs
- Converts score lists + weights to layer score dictionaries
- Preserves non-linear interaction semantics from Choquet integral

References:
- Grabisch, M. (2016). "Set Functions, Games and Capacities in Decision Making"
- Choquet, G. (1953). "Theory of capacities"
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class ChoquetProcessingAdapter:
    """
    Adapter for using Choquet integral in processing aggregation.
    
    This class bridges the gap between calibration (layer-based) and
    processing (score list) contexts.
    """
    
    def __init__(
        self,
        linear_weights: dict[str, float] | None = None,
        interaction_weights: dict[tuple[str, str], float] | None = None,
    ):
        """
        Initialize Choquet adapter.
        
        Args:
            linear_weights: Weights for linear terms (default: uniform)
            interaction_weights: Weights for interaction terms (default: none)
        """
        self.linear_weights = linear_weights or {}
        self.interaction_weights = interaction_weights or {}
        logger.info(
            f"ChoquetProcessingAdapter initialized: "
            f"{len(self.linear_weights)} linear, "
            f"{len(self.interaction_weights)} interaction terms"
        )
    
    def aggregate(
        self,
        scores: list[float],
        weights: list[float] | None = None,
        interaction_pairs: list[tuple[int, int]] | None = None,
    ) -> float:
        """
        Aggregate scores using Choquet 2-additive integral.
        
        Formula:
            C(x) = Σ w_i * x_i + Σ w_ij * min(x_i, x_j)
        
        Where:
        - First sum: Linear terms (weighted individual scores)
        - Second sum: Interaction terms (synergy/redundancy between pairs)
        
        Args:
            scores: List of numeric scores
            weights: Linear weights for each score (default: uniform)
            interaction_pairs: List of (i, j) index pairs for interactions
        
        Returns:
            Aggregated score
        
        Raises:
            ValueError: If weights mismatch or scores empty
        """
        if not scores:
            raise ValueError("Cannot aggregate empty score list")
        
        n = len(scores)
        scores_arr = np.array(scores, dtype=np.float64)
        
        # Default: uniform weights
        if weights is None:
            weights_arr = np.ones(n) / n
        else:
            if len(weights) != n:
                raise ValueError(f"Weight count {len(weights)} != score count {n}")
            weights_arr = np.array(weights, dtype=np.float64)
            # Normalize to sum to 1.0
            weights_arr = weights_arr / np.sum(weights_arr)
        
        # STEP 1: Linear contribution
        # C_linear = Σ w_i * x_i
        linear_contrib = float(np.sum(weights_arr * scores_arr))
        
        logger.debug(f"Choquet linear contribution: {linear_contrib:.4f}")
        
        # STEP 2: Interaction contribution
        # C_interaction = Σ w_ij * min(x_i, x_j)
        interaction_contrib = 0.0
        
        if interaction_pairs:
            for i, j in interaction_pairs:
                if i >= n or j >= n:
                    logger.warning(f"Interaction pair ({i}, {j}) out of bounds (n={n})")
                    continue
                
                # Interaction weight (default: small positive for synergy)
                pair_key = (str(i), str(j))
                w_ij = self.interaction_weights.get(pair_key, 0.05)
                
                # Choquet uses min() for weakest-link principle
                min_score = min(scores_arr[i], scores_arr[j])
                contribution = w_ij * min_score
                interaction_contrib += contribution
                
                logger.debug(
                    f"Interaction ({i}, {j}): "
                    f"min({scores_arr[i]:.2f}, {scores_arr[j]:.2f}) = {min_score:.2f}, "
                    f"w={w_ij:.3f}, contrib={contribution:.4f}"
                )
        
        logger.debug(f"Choquet interaction contribution: {interaction_contrib:.4f}")
        
        # STEP 3: Total score
        total = linear_contrib + interaction_contrib
        
        logger.info(
            f"Choquet aggregation: {n} inputs → {total:.4f} "
            f"(linear={linear_contrib:.4f}, interaction={interaction_contrib:.4f})"
        )
        
        return float(total)
    
    @staticmethod
    def detect_interactions(
        scores: list[float],
        weights: list[float],
        correlation_threshold: float = 0.7,
    ) -> list[tuple[int, int]]:
        """
        Auto-detect interaction pairs based on score correlation.
        
        Pairs with high correlation should be penalized (redundancy),
        pairs with negative correlation should be rewarded (complementarity).
        
        Args:
            scores: Score values
            weights: Score weights
            correlation_threshold: Min correlation for interaction
        
        Returns:
            List of (i, j) pairs with significant interactions
        
        Note:
            This is a heuristic. For production, use domain knowledge to
            specify interactions explicitly.
        """
        n = len(scores)
        pairs = []
        
        # For now, use a simple heuristic: top-weighted pairs
        # In practice, you'd analyze historical data for correlations
        sorted_indices = np.argsort(weights)[::-1]  # Descending
        
        # Consider top 3 interactions among high-weight inputs
        if n >= 2:
            for i in range(min(3, n - 1)):
                idx_i = sorted_indices[i]
                idx_j = sorted_indices[i + 1]
                pairs.append((int(idx_i), int(idx_j)))
        
        logger.debug(f"Auto-detected {len(pairs)} interaction pairs")
        return pairs


def create_default_choquet_adapter(n_inputs: int) -> ChoquetProcessingAdapter:
    """
    Create a Choquet adapter with sensible defaults.
    
    Default configuration:
    - Uniform linear weights (each input gets 1/n)
    - Small interaction weights (0.05) for adjacent pairs
    - Synergistic interactions (positive weights)
    
    Args:
        n_inputs: Number of input scores
    
    Returns:
        Configured ChoquetProcessingAdapter
    """
    # Linear weights: uniform
    linear_weights = {str(i): 1.0 / n_inputs for i in range(n_inputs)}
    
    # Interaction weights: adjacent pairs only (locality assumption)
    interaction_weights = {}
    for i in range(n_inputs - 1):
        pair_key = (str(i), str(i + 1))
        interaction_weights[pair_key] = 0.05  # Small synergy
    
    logger.info(
        f"Created default Choquet adapter: "
        f"{n_inputs} inputs, {len(interaction_weights)} interactions"
    )
    
    return ChoquetProcessingAdapter(
        linear_weights=linear_weights,
        interaction_weights=interaction_weights,
    )


__all__ = [
    "ChoquetProcessingAdapter",
    "create_default_choquet_adapter",
]
