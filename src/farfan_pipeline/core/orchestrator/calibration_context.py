"""
calibration_context.py - Calibration Context Data Structure

This module defines the CalibrationContext dataclass that encapsulates all
contextual information needed for method calibration. It serves as the
canonical context container for the calibration system.

Architectural Constraints:
- [Constraint 1] Factory method validates question IDs against canonical catalog
- Provides stable hash generation for caching layer (Component 4)
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class CalibrationContext:
    """
    Immutable context for method calibration.
    
    Fields:
        question_id: Question identifier (e.g., "D3-Q2")
        dimension: Dimension number (1-6)
        policy_area: Policy area identifier
        unit_quality: Unit-of-analysis quality score [0,1]
        method_position: Position of method in execution chain (1-indexed)
        total_methods: Total number of methods in execution chain
        question_num: Question number within dimension (1-5)
        
    Example:
        >>> ctx = CalibrationContext.from_question_id("D3-Q2", unit_quality=0.85)
        >>> ctx.dimension
        3
        >>> ctx.question_num
        2
    """
    
    question_id: str
    dimension: int
    policy_area: Optional[str] = None
    unit_quality: float = 1.0
    method_position: int = 1
    total_methods: int = 1
    question_num: int = field(init=False)
    
    def __post_init__(self):
        """Validate and extract question_num from question_id."""
        # Extract question number from question_id
        match = re.match(r"D(\d+)-Q(\d+)", self.question_id)
        if not match:
            raise ValueError(
                f"Invalid question_id format: {self.question_id}. "
                f"Expected format: D{{n}}-Q{{m}} (e.g., 'D3-Q2')"
            )
        
        dimension_from_id = int(match.group(1))
        question_num = int(match.group(2))
        
        # Validate dimension consistency
        if dimension_from_id != self.dimension:
            raise ValueError(
                f"Dimension mismatch: question_id has D{dimension_from_id} "
                f"but dimension={self.dimension}"
            )
        
        # Validate ranges
        if not (1 <= self.dimension <= 6):
            raise ValueError(f"Dimension must be 1-6, got {self.dimension}")
        
        if not (1 <= question_num <= 5):
            raise ValueError(f"Question number must be 1-5, got {question_num}")
        
        if not (0 <= self.unit_quality <= 1):
            raise ValueError(
                f"unit_quality must be in [0,1], got {self.unit_quality}"
            )
        
        if self.method_position < 1 or self.method_position > self.total_methods:
            raise ValueError(
                f"method_position ({self.method_position}) must be in "
                f"[1, {self.total_methods}]"
            )
        
        # Use object.__setattr__ since dataclass is frozen
        object.__setattr__(self, 'question_num', question_num)
    
    @classmethod
    def from_question_id(
        cls,
        question_id: str,
        policy_area: Optional[str] = None,
        unit_quality: float = 1.0,
        method_position: int = 1,
        total_methods: int = 1,
    ) -> CalibrationContext:
        """
        Factory method to create context from question ID.
        
        Automatically extracts dimension and question numbers from ID format.
        
        Args:
            question_id: Question identifier (e.g., "D3-Q2")
            policy_area: Optional policy area identifier
            unit_quality: Unit-of-analysis quality score [0,1]
            method_position: Position in execution chain (1-indexed)
            total_methods: Total methods in execution chain
            
        Returns:
            CalibrationContext instance
            
        Raises:
            ValueError: If question_id format is invalid
            
        Example:
            >>> ctx = CalibrationContext.from_question_id(
            ...     "D3-Q2",
            ...     policy_area="education",
            ...     unit_quality=0.85
            ... )
        """
        # Extract dimension from question_id
        match = re.match(r"D(\d+)-Q(\d+)", question_id)
        if not match:
            raise ValueError(
                f"Invalid question_id format: {question_id}. "
                f"Expected format: D{{n}}-Q{{m}} (e.g., 'D3-Q2')"
            )
        
        dimension = int(match.group(1))
        
        return cls(
            question_id=question_id,
            dimension=dimension,
            policy_area=policy_area,
            unit_quality=unit_quality,
            method_position=method_position,
            total_methods=total_methods,
        )
    
    def to_stable_hash(self) -> str:
        """
        Generate stable hash for caching (Component 4).
        
        Uses all fields except transient metadata (method_position, total_methods)
        to create a deterministic cache key.
        
        Returns:
            SHA256 hex digest
            
        Example:
            >>> ctx1 = CalibrationContext.from_question_id("D3-Q2", unit_quality=0.85)
            >>> ctx2 = CalibrationContext.from_question_id("D3-Q2", unit_quality=0.85)
            >>> ctx1.to_stable_hash() == ctx2.to_stable_hash()
            True
        """
        # Only hash fields that affect calibration semantics
        # Exclude method_position and total_methods (execution metadata)
        hash_input = (
            f"qid={self.question_id}|"
            f"dim={self.dimension}|"
            f"policy={self.policy_area}|"
            f"unit_q={self.unit_quality:.6f}|"
            f"q_num={self.question_num}"
        )
        
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"CalibrationContext("
            f"question_id='{self.question_id}', "
            f"dimension={self.dimension}, "
            f"question_num={self.question_num}, "
            f"unit_quality={self.unit_quality:.3f})"
        )
