"""SPC to Orchestrator Adapter.

This adapter converts Smart Policy Chunks (SPC) / Canon Policy Package (CPP)
documents from the ingestion pipeline into the orchestrator's PreprocessedDocument format.

Note: SPC is the new terminology for CPP (Canon Policy Package). This module provides
compatibility by aliasing to the existing CPPAdapter implementation.

Design Principles:
- Preserves complete provenance information
- Orders chunks by text_span.start for deterministic ordering
- Computes provenance_completeness metric
- Provides prescriptive error messages on failure
- Supports micro, meso, and macro chunk resolutions
- Optional dependencies handled gracefully (pyarrow, structlog)
"""

from __future__ import annotations

from saaaaaa.utils.cpp_adapter import (
    CPPAdapter,
    CPPAdapterError,
    adapt_cpp_to_orchestrator,
)

# Alias for terminology consistency - SPC is the new name for CPP
SPCAdapter = CPPAdapter
SPCAdapterError = CPPAdapterError


def adapt_spc_to_orchestrator(*args, **kwargs):
    """
    Convert Smart Policy Chunks (SPC) documents to orchestrator format.

    This is an alias for adapt_cpp_to_orchestrator, provided for terminology
    consistency as SPC (Smart Policy Chunks) is the new name for CPP (Canon
    Policy Package).

    The adapter performs the following transformations:
    - Converts SPC/CPP document structure to PreprocessedDocument format
    - Preserves complete provenance information for traceability
    - Orders chunks by text_span.start for deterministic ordering
    - Computes provenance_completeness metric
    - Supports micro, meso, and macro chunk resolutions

    Args:
        *args: Positional arguments passed to adapt_cpp_to_orchestrator
        **kwargs: Keyword arguments passed to adapt_cpp_to_orchestrator

    Returns:
        PreprocessedDocument: Document formatted for orchestrator consumption

    Raises:
        SPCAdapterError: If document conversion fails

    See Also:
        adapt_cpp_to_orchestrator: The underlying implementation function
        CPPAdapter: The adapter class for more control over the conversion process
    """
    return adapt_cpp_to_orchestrator(*args, **kwargs)


__all__ = [
    'SPCAdapter',
    'SPCAdapterError',
    'adapt_spc_to_orchestrator',
]
