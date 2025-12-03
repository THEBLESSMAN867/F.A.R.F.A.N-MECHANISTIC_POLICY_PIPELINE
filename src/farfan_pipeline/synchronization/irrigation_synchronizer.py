"""Irrigation synchronization and chunk matrix validation for policy analysis."""

import re

from farfan_pipeline.core.types import ChunkData, PreprocessedDocument


class ChunkMatrix:
    """Validates and provides O(1) access to policy chunks organized by area × dimension.

    Ensures exactly 60 unique chunks covering all PA01-PA10 × DIM01-DIM06 combinations
    with proper ID formatting and non-null metadata.
    """

    POLICY_AREAS = [f"PA{i:02d}" for i in range(1, 11)]
    DIMENSIONS = [f"DIM{i:02d}" for i in range(1, 7)]
    EXPECTED_CHUNK_COUNT = 60
    CHUNK_ID_PATTERN = re.compile(r"^PA(0[1-9]|10)-DIM0[1-6]$")

    def __init__(self, document: PreprocessedDocument) -> None:
        self._matrix: dict[tuple[str, str], ChunkData] = {}
        self._build_and_validate(document)

    def _build_and_validate(self, document: PreprocessedDocument) -> None:
        """Construct matrix from document chunks and validate completeness.

        Args:
            document: PreprocessedDocument containing chunks to validate

        Raises:
            ValueError: If chunk count != 60, duplicate keys exist, missing combinations,
                       null IDs, or invalid chunk_id format
        """
        seen_keys: set[tuple[str, str]] = set()

        for chunk in document.chunks:
            if chunk.policy_area_id is None:
                raise ValueError(f"Chunk {chunk.id} has null policy_area_id")
            if chunk.dimension_id is None:
                raise ValueError(f"Chunk {chunk.id} has null dimension_id")

            chunk_id = f"{chunk.policy_area_id}-{chunk.dimension_id}"
            if not self.CHUNK_ID_PATTERN.match(chunk_id):
                raise ValueError(
                    f"Invalid chunk_id format: '{chunk_id}' "
                    f"(expected PA{{01-10}}-DIM{{01-06}})"
                )

            key = (chunk.policy_area_id, chunk.dimension_id)

            if key in seen_keys:
                raise ValueError(f"Duplicate key detected: {key[0]}-{key[1]}")

            seen_keys.add(key)
            self._matrix[key] = chunk

        expected_keys = {
            (pa, dim) for pa in self.POLICY_AREAS for dim in self.DIMENSIONS
        }
        missing_keys = expected_keys - seen_keys

        if missing_keys:
            missing_formatted = sorted(f"{pa}-{dim}" for pa, dim in missing_keys)
            raise ValueError(
                f"Missing required chunk combinations: {', '.join(missing_formatted)}"
            )

        if len(document.chunks) != self.EXPECTED_CHUNK_COUNT:
            raise ValueError(
                f"Expected exactly {self.EXPECTED_CHUNK_COUNT} chunks, "
                f"got {len(document.chunks)}"
            )

    def get_chunk(self, policy_area_id: str, dimension_id: str) -> ChunkData:
        """Retrieve chunk by policy area and dimension with O(1) lookup.

        Args:
            policy_area_id: Policy area identifier (PA01-PA10)
            dimension_id: Dimension identifier (DIM01-DIM06)

        Returns:
            ChunkData for the specified combination

        Raises:
            KeyError: If the combination does not exist
        """
        key = (policy_area_id, dimension_id)
        if key not in self._matrix:
            raise KeyError(f"Chunk not found for key: {policy_area_id}-{dimension_id}")
        return self._matrix[key]
