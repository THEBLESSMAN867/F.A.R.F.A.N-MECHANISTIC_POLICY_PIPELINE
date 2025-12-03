"""Infrastructure package - Adapters for ports.

This package contains concrete implementations of port interfaces.
Adapters handle external dependencies like file systems, databases, and APIs.

Structure:
- filesystem.py: File system operations
- environment.py: Environment variable access
- clock.py: Time operations
- log_adapters.py: Logging operations (renamed from logging.py to avoid shadowing)
- recommendation_engine_adapter.py: Recommendation engine adapter
"""

from farfan_pipeline.infrastructure.recommendation_engine_adapter import (
    RecommendationEngineAdapter,
    create_recommendation_engine_adapter,
)

__all__ = [
    "RecommendationEngineAdapter",
    "create_recommendation_engine_adapter",
]
