"""Chunk matrix construction and validation for policy analysis pipeline.

This module provides deterministic construction of the 60-chunk PA×DIM matrix
with comprehensive validation, duplicate detection, and audit logging.
"""

import logging
import re
from collections.abc import Iterable

from farfan_pipeline.core.types import ChunkData, PreprocessedDocument

logger = logging.getLogger(__name__)

POLICY_AREAS = [f"PA{i:02d}" for i in range(1, 11)]
DIMENSIONS = [f"DIM{i:02d}" for i in range(1, 7)]
EXPECTED_CHUNK_COUNT = 60
CHUNK_ID_PATTERN = re.compile(r"^PA(0[1-9]|10)-DIM0[1-6]$")
MAX_MISSING_KEYS_TO_DISPLAY = 10


def build_chunk_matrix(
    document: PreprocessedDocument,
) -> tuple[dict[tuple[str, str], ChunkData], list[tuple[str, str]]]:
    """Construct validated chunk matrix from preprocessed document.

    Builds a dictionary mapping (PA, DIM) tuples to SmartPolicyChunk instances,
    performs comprehensive validation, and returns sorted keys for deterministic
    iteration.

    Args:
        document: PreprocessedDocument containing 60 policy chunks

    Returns:
        Tuple of (chunk_matrix, sorted_keys) where:
        - chunk_matrix: dict mapping (PA, DIM) -> ChunkData
        - sorted_keys: list of (PA, DIM) tuples sorted deterministically

    Raises:
        ValueError: If validation fails (wrong count, duplicates, missing combinations,
                   null IDs, or invalid chunk_id format)

    Example:
        >>> doc = PreprocessedDocument(...)
        >>> matrix, keys = build_chunk_matrix(doc)
        >>> chunk = matrix[("PA01", "DIM01")]
        >>> assert len(keys) == 60
        >>> assert keys[0] == ("PA01", "DIM01")
    """
    logger.info(
        f"Building chunk matrix from document {document.document_id} "
        f"with {len(document.chunks)} chunks"
    )

    matrix: dict[tuple[str, str], ChunkData] = {}
    seen_keys: set[tuple[str, str]] = set()
    seen_chunk_ids: set[str] = set()

    for idx, chunk in enumerate(document.chunks):
        _validate_chunk_metadata(chunk, idx)

        assert chunk.policy_area_id is not None
        assert chunk.dimension_id is not None

        chunk_id = f"{chunk.policy_area_id}-{chunk.dimension_id}"
        _validate_chunk_id_format(chunk_id, idx)

        key = (chunk.policy_area_id, chunk.dimension_id)

        _check_duplicate_key(key, seen_keys, chunk_id)
        _check_duplicate_chunk_id(chunk_id, seen_chunk_ids, idx)

        seen_keys.add(key)
        seen_chunk_ids.add(chunk_id)
        matrix[key] = chunk

    _validate_completeness(seen_keys)
    _validate_chunk_count(document.chunks, EXPECTED_CHUNK_COUNT)

    sorted_keys = _sort_keys_deterministically(matrix.keys())

    logger.info(
        f"Chunk matrix constructed successfully: {len(matrix)} chunks, "
        f"{len(sorted_keys)} unique keys"
    )
    _log_audit_summary(matrix, sorted_keys)

    return matrix, sorted_keys


def _validate_chunk_metadata(chunk: ChunkData, idx: int) -> None:
    """Validate chunk has required metadata fields.

    Args:
        chunk: ChunkData to validate
        idx: Chunk index for error reporting

    Raises:
        ValueError: If policy_area_id or dimension_id is None
    """
    if chunk.policy_area_id is None:
        raise ValueError(
            f"Chunk at index {idx} (id={chunk.id}) has null policy_area_id"
        )
    if chunk.dimension_id is None:
        raise ValueError(f"Chunk at index {idx} (id={chunk.id}) has null dimension_id")


def _validate_chunk_id_format(chunk_id: str, idx: int) -> None:
    """Validate chunk_id matches PA{01-10}-DIM{01-06} pattern.

    Args:
        chunk_id: Chunk identifier to validate
        idx: Chunk index for error reporting

    Raises:
        ValueError: If chunk_id format is invalid
    """
    if not CHUNK_ID_PATTERN.match(chunk_id):
        raise ValueError(
            f"Invalid chunk_id format at index {idx}: '{chunk_id}' "
            f"(expected PA{{01-10}}-DIM{{01-06}})"
        )


def _check_duplicate_key(
    key: tuple[str, str],
    seen_keys: set[tuple[str, str]],
    chunk_id: str,
) -> None:
    """Check for duplicate (PA, DIM) keys.

    Args:
        key: (policy_area_id, dimension_id) tuple
        seen_keys: Set of previously seen keys
        chunk_id: Chunk identifier for error reporting

    Raises:
        ValueError: If key already exists in seen_keys
    """
    if key in seen_keys:
        raise ValueError(
            f"Duplicate (PA, DIM) combination detected: {chunk_id}. "
            f"Each PA×DIM combination must appear exactly once."
        )


def _check_duplicate_chunk_id(
    chunk_id: str,
    seen_chunk_ids: set[str],
    idx: int,
) -> None:
    """Check for duplicate chunk_id strings.

    Args:
        chunk_id: Chunk identifier to check
        seen_chunk_ids: Set of previously seen chunk IDs
        idx: Chunk index for error reporting

    Raises:
        ValueError: If chunk_id already exists
    """
    if chunk_id in seen_chunk_ids:
        raise ValueError(
            f"Duplicate chunk_id detected at index {idx}: '{chunk_id}'. "
            f"Each chunk must have a unique identifier."
        )


def _validate_chunk_count(
    chunks: list[ChunkData],
    expected_count: int,
) -> None:
    """Validate document has exactly the expected number of chunks.

    Args:
        chunks: List of chunks from document
        expected_count: Expected number of chunks (60)

    Raises:
        ValueError: If chunk count doesn't match expectation
    """
    actual_count = len(chunks)
    if actual_count != expected_count:
        raise ValueError(
            f"Expected exactly {expected_count} chunks, got {actual_count}. "
            f"Policy matrix requires PA01-PA10 × DIM01-DIM06 = 60 unique chunks."
        )


def _validate_completeness(seen_keys: set[tuple[str, str]]) -> None:
    """Validate all required PA×DIM combinations are present.

    Args:
        seen_keys: Set of (PA, DIM) keys found in document

    Raises:
        ValueError: If any required combinations are missing
    """
    expected_keys = {(pa, dim) for pa in POLICY_AREAS for dim in DIMENSIONS}
    missing_keys = expected_keys - seen_keys

    if missing_keys:
        missing_formatted = sorted(f"{pa}-{dim}" for pa, dim in missing_keys)
        truncated_list = missing_formatted[:MAX_MISSING_KEYS_TO_DISPLAY]
        suffix = (
            f"... and {len(missing_keys) - MAX_MISSING_KEYS_TO_DISPLAY} more"
            if len(missing_keys) > MAX_MISSING_KEYS_TO_DISPLAY
            else ""
        )
        raise ValueError(
            f"Missing {len(missing_keys)} required PA×DIM combinations: "
            f"{', '.join(truncated_list)}{suffix}"
        )


def _sort_keys_deterministically(
    keys: Iterable[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Sort matrix keys deterministically by PA then DIM.

    Args:
        keys: Iterable of (PA, DIM) tuple keys

    Returns:
        Sorted list of keys for deterministic iteration
    """
    return sorted(keys, key=lambda k: (k[0], k[1]))


def _log_audit_summary(
    matrix: dict[tuple[str, str], ChunkData],
    sorted_keys: list[tuple[str, str]],
) -> None:
    """Log audit summary of constructed matrix.

    Args:
        matrix: Constructed chunk matrix
        sorted_keys: Sorted list of matrix keys
    """
    pa_counts: dict[str, int] = {}
    dim_counts: dict[str, int] = {}

    for pa, dim in sorted_keys:
        pa_counts[pa] = pa_counts.get(pa, 0) + 1
        dim_counts[dim] = dim_counts.get(dim, 0) + 1

    total_text_length = sum(len(chunk.text) for chunk in matrix.values())
    avg_text_length = total_text_length // len(matrix) if matrix else 0

    logger.info(
        f"Chunk matrix audit: PA coverage={len(pa_counts)}/10, "
        f"DIM coverage={len(dim_counts)}/6, "
        f"total_text_chars={total_text_length}, "
        f"avg_chunk_length={avg_text_length}"
    )

    first_key = sorted_keys[0] if sorted_keys else None
    last_key = sorted_keys[-1] if sorted_keys else None
    logger.debug(f"Matrix key range: first={first_key}, last={last_key}")
