"""
Comprehensive test suite for ExecutionMap contract validation.

These tests serve as CI-blocking guarantees of routing correctness.
Any failure represents a critical regression and must prevent code merges.
"""

import json

import pytest

from farfan_pipeline.core.orchestrator.chunk_router import (
    ChunkRoute,
    ChunkRouter,
    compute_execution_map_hash,
    deserialize_execution_map,
    serialize_execution_map,
)
from farfan_pipeline.core.types import ChunkData


@pytest.fixture
def chunk_router():
    return ChunkRouter()


class TestContractValidation:
    """Verify ExecutionMap object validity and contract compliance."""

    def test_generate_execution_map_returns_valid_structure(self, chunk_router):
        chunks = [
            ChunkData(
                id=1,
                text="Test",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=4,
                confidence=1.0,
            )
        ]

        execution_map = chunk_router.generate_execution_map(chunks)

        assert isinstance(execution_map, dict)
        assert len(execution_map) == 1
        assert 1 in execution_map
        assert isinstance(execution_map[1], ChunkRoute)

    def test_chunk_route_has_required_fields(self, chunk_router):
        chunk = ChunkData(
            id=42,
            text="Test chunk",
            chunk_type="activity",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=10,
            confidence=0.9,
        )

        route = chunk_router.route_chunk(chunk)

        assert hasattr(route, "chunk_id")
        assert hasattr(route, "chunk_type")
        assert hasattr(route, "executor_class")
        assert hasattr(route, "methods")
        assert hasattr(route, "skip_reason")
        assert route.chunk_id == 42
        assert route.chunk_type == "activity"

    def test_execution_map_with_mixed_chunk_types(self, chunk_router):
        chunks = [
            ChunkData(
                id=1,
                text="Diagnostic",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=10,
                confidence=1.0,
            ),
            ChunkData(
                id=2,
                text="Activity",
                chunk_type="activity",
                sentences=[],
                tables=[],
                start_pos=11,
                end_pos=20,
                confidence=1.0,
            ),
            ChunkData(
                id=3,
                text="Indicator",
                chunk_type="indicator",
                sentences=[],
                tables=[],
                start_pos=21,
                end_pos=30,
                confidence=1.0,
            ),
        ]

        execution_map = chunk_router.generate_execution_map(chunks)

        assert len(execution_map) == 3
        assert all(isinstance(route, ChunkRoute) for route in execution_map.values())
        assert execution_map[1].chunk_type == "diagnostic"
        assert execution_map[2].chunk_type == "activity"
        assert execution_map[3].chunk_type == "indicator"


class TestSerializationContract:
    """Verify serialization/deserialization is lossless and correct."""

    def test_serialize_execution_map_produces_valid_json(self, chunk_router):
        chunks = [
            ChunkData(
                id=1,
                text="Test",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=4,
                confidence=1.0,
            )
        ]

        execution_map = chunk_router.generate_execution_map(chunks)
        serialized = serialize_execution_map(execution_map)

        parsed = json.loads(serialized)
        assert "version" in parsed
        assert "routes" in parsed
        assert isinstance(parsed["routes"], dict)

    def test_serialize_deserialize_roundtrip_preserves_data(self, chunk_router):
        chunks = [
            ChunkData(
                id=10,
                text="Diagnostic chunk",
                chunk_type="diagnostic",
                sentences=[1, 2],
                tables=[],
                start_pos=0,
                end_pos=16,
                confidence=0.95,
                policy_area_id="PA05",
                dimension_id="DIM01",
            ),
            ChunkData(
                id=20,
                text="Activity chunk",
                chunk_type="activity",
                sentences=[3],
                tables=[1],
                start_pos=17,
                end_pos=31,
                confidence=0.88,
                policy_area_id="PA03",
                dimension_id="DIM02",
            ),
        ]

        original_map = chunk_router.generate_execution_map(chunks)
        serialized = serialize_execution_map(original_map)
        restored_map = deserialize_execution_map(serialized)

        assert len(restored_map) == len(original_map)
        assert set(restored_map.keys()) == set(original_map.keys())

        for chunk_id in original_map:
            orig_route = original_map[chunk_id]
            rest_route = restored_map[chunk_id]

            assert orig_route.chunk_id == rest_route.chunk_id
            assert orig_route.chunk_type == rest_route.chunk_type
            assert orig_route.executor_class == rest_route.executor_class
            assert orig_route.methods == rest_route.methods
            assert orig_route.skip_reason == rest_route.skip_reason

    def test_deserialize_rejects_invalid_json(self):
        invalid_json = "{ invalid json }"
        with pytest.raises(ValueError, match="Invalid JSON format"):
            deserialize_execution_map(invalid_json)

    def test_deserialize_rejects_wrong_version(self):
        wrong_version = json.dumps({"version": "v999", "routes": {}})
        with pytest.raises(ValueError, match="Invalid or unsupported version"):
            deserialize_execution_map(wrong_version)

    def test_deserialize_rejects_missing_routes(self):
        missing_routes = json.dumps({"version": "v1"})
        with pytest.raises(ValueError, match="Missing 'routes' key"):
            deserialize_execution_map(missing_routes)

    def test_deserialize_rejects_invalid_chunk_id(self):
        invalid_id = json.dumps(
            {
                "version": "v1",
                "routes": {
                    "not_an_int": {
                        "chunk_id": 1,
                        "chunk_type": "diagnostic",
                        "executor_class": "D1Q1",
                        "methods": [],
                        "skip_reason": None,
                    }
                },
            }
        )
        with pytest.raises(ValueError, match="Invalid chunk_id"):
            deserialize_execution_map(invalid_id)

    def test_serialize_produces_deterministic_output(self, chunk_router):
        chunks = [
            ChunkData(
                id=5,
                text="Test",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=4,
                confidence=1.0,
            )
        ]

        execution_map = chunk_router.generate_execution_map(chunks)

        serialized1 = serialize_execution_map(execution_map)
        serialized2 = serialize_execution_map(execution_map)

        assert serialized1 == serialized2


class TestDeterminismContract:
    """Verify ExecutionMap generation is completely deterministic."""

    def test_multiple_runs_produce_identical_maps(self, chunk_router):
        chunks = [
            ChunkData(
                id=1,
                text="Test diagnostic",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=15,
                confidence=0.9,
            ),
            ChunkData(
                id=2,
                text="Test activity",
                chunk_type="activity",
                sentences=[],
                tables=[],
                start_pos=16,
                end_pos=29,
                confidence=0.85,
            ),
        ]

        maps = [chunk_router.generate_execution_map(chunks) for _ in range(10)]

        first_map = maps[0]
        for subsequent_map in maps[1:]:
            assert list(first_map.keys()) == list(subsequent_map.keys())
            for chunk_id in first_map:
                assert first_map[chunk_id] == subsequent_map[chunk_id]

    def test_map_hash_is_deterministic(self, chunk_router):
        chunks = [
            ChunkData(
                id=7,
                text="Test",
                chunk_type="resource",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=4,
                confidence=1.0,
            )
        ]

        execution_map = chunk_router.generate_execution_map(chunks)

        hashes = [compute_execution_map_hash(execution_map) for _ in range(5)]

        assert len(set(hashes)) == 1

    def test_input_order_does_not_affect_determinism(self, chunk_router):
        chunk1 = ChunkData(
            id=100,
            text="First",
            chunk_type="diagnostic",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=5,
            confidence=1.0,
        )
        chunk2 = ChunkData(
            id=200,
            text="Second",
            chunk_type="activity",
            sentences=[],
            tables=[],
            start_pos=6,
            end_pos=12,
            confidence=1.0,
        )

        map_order1 = chunk_router.generate_execution_map([chunk1, chunk2])
        map_order2 = chunk_router.generate_execution_map([chunk2, chunk1])

        hash1 = compute_execution_map_hash(map_order1)
        hash2 = compute_execution_map_hash(map_order2)

        assert hash1 == hash2

    def test_determinism_with_policy_area_and_dimension(self, chunk_router):
        chunks = [
            ChunkData(
                id=1,
                text="Chunk 1",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=7,
                confidence=1.0,
                policy_area_id="PA05",
                dimension_id="DIM02",
            ),
            ChunkData(
                id=2,
                text="Chunk 2",
                chunk_type="activity",
                sentences=[],
                tables=[],
                start_pos=8,
                end_pos=15,
                confidence=1.0,
                policy_area_id="PA03",
                dimension_id="DIM04",
            ),
        ]

        hashes = [
            compute_execution_map_hash(chunk_router.generate_execution_map(chunks))
            for _ in range(10)
        ]

        assert len(set(hashes)) == 1


class TestCorrectnessContract:
    """Verify routing correctness for specific policy_area and dimension combinations."""

    @pytest.mark.parametrize(
        "chunk_type,expected_executor",
        [
            ("diagnostic", "D1Q1"),
            ("activity", "D2Q1"),
            ("indicator", "D3Q1"),
            ("resource", "D1Q3"),
            ("temporal", "D1Q5"),
            ("entity", "D2Q3"),
        ],
    )
    def test_chunk_type_maps_to_correct_primary_executor(
        self, chunk_router, chunk_type, expected_executor
    ):
        chunk = ChunkData(
            id=1,
            text="Test",
            chunk_type=chunk_type,
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=4,
            confidence=1.0,
        )

        route = chunk_router.route_chunk(chunk)

        assert route.executor_class == expected_executor
        assert route.skip_reason is None

    def test_pa05_dim02_routes_correctly(self, chunk_router):
        chunk = ChunkData(
            id=1,
            text="PA05 + DIM02 specific content",
            chunk_type="activity",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=29,
            confidence=0.95,
            policy_area_id="PA05",
            dimension_id="DIM02",
        )

        route = chunk_router.route_chunk(chunk)

        assert route.executor_class == "D2Q1"
        assert route.skip_reason is None

    def test_unknown_chunk_type_produces_skip_reason(self, chunk_router):
        chunk = ChunkData(
            id=999,
            text="Unknown type",
            chunk_type="unknown_type",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=12,
            confidence=0.5,
        )

        route = chunk_router.route_chunk(chunk)

        assert route.executor_class == ""
        assert route.skip_reason is not None
        assert "No executor mapping" in route.skip_reason

    def test_multiple_pa_dim_combinations_route_exclusively(self, chunk_router):
        chunks = [
            ChunkData(
                id=1,
                text="PA01 DIM01",
                chunk_type="diagnostic",
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=10,
                confidence=1.0,
                policy_area_id="PA01",
                dimension_id="DIM01",
            ),
            ChunkData(
                id=2,
                text="PA05 DIM02",
                chunk_type="activity",
                sentences=[],
                tables=[],
                start_pos=11,
                end_pos=21,
                confidence=1.0,
                policy_area_id="PA05",
                dimension_id="DIM02",
            ),
            ChunkData(
                id=3,
                text="PA10 DIM06",
                chunk_type="indicator",
                sentences=[],
                tables=[],
                start_pos=22,
                end_pos=32,
                confidence=1.0,
                policy_area_id="PA10",
                dimension_id="DIM06",
            ),
        ]

        execution_map = chunk_router.generate_execution_map(chunks)

        assert execution_map[1].executor_class == "D1Q1"
        assert execution_map[2].executor_class == "D2Q1"
        assert execution_map[3].executor_class == "D3Q1"

        executors = {route.executor_class for route in execution_map.values()}
        assert len(executors) == 3

    def test_routing_table_completeness(self, chunk_router):
        valid_chunk_types = [
            "diagnostic",
            "activity",
            "indicator",
            "resource",
            "temporal",
            "entity",
        ]

        for chunk_type in valid_chunk_types:
            chunk = ChunkData(
                id=1,
                text=f"Test {chunk_type}",
                chunk_type=chunk_type,
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=10,
                confidence=1.0,
            )

            route = chunk_router.route_chunk(chunk)

            assert route.executor_class != ""
            assert route.skip_reason is None


class TestEdgeCasesContract:
    """Verify router behavior with malformed or incomplete chunk metadata."""

    def test_chunk_with_none_policy_area(self, chunk_router):
        chunk = ChunkData(
            id=1,
            text="Test",
            chunk_type="diagnostic",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=4,
            confidence=1.0,
            policy_area_id=None,
            dimension_id="DIM01",
        )

        route = chunk_router.route_chunk(chunk)

        assert isinstance(route, ChunkRoute)
        assert route.executor_class == "D1Q1"

    def test_chunk_with_none_dimension(self, chunk_router):
        chunk = ChunkData(
            id=1,
            text="Test",
            chunk_type="activity",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=4,
            confidence=1.0,
            policy_area_id="PA05",
            dimension_id=None,
        )

        route = chunk_router.route_chunk(chunk)

        assert isinstance(route, ChunkRoute)
        assert route.executor_class == "D2Q1"

    def test_empty_chunk_list(self, chunk_router):
        execution_map = chunk_router.generate_execution_map([])

        assert execution_map == {}

    def test_chunk_with_zero_confidence(self, chunk_router):
        chunk = ChunkData(
            id=1,
            text="Low confidence",
            chunk_type="diagnostic",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=14,
            confidence=0.0,
        )

        route = chunk_router.route_chunk(chunk)

        assert isinstance(route, ChunkRoute)
        assert route.executor_class == "D1Q1"

    def test_chunk_with_negative_positions(self, chunk_router):
        chunk = ChunkData(
            id=1,
            text="Negative positions",
            chunk_type="activity",
            sentences=[],
            tables=[],
            start_pos=-10,
            end_pos=-1,
            confidence=1.0,
        )

        route = chunk_router.route_chunk(chunk)

        assert isinstance(route, ChunkRoute)

    def test_chunk_with_empty_text(self, chunk_router):
        chunk = ChunkData(
            id=1,
            text="",
            chunk_type="indicator",
            sentences=[],
            tables=[],
            start_pos=0,
            end_pos=0,
            confidence=1.0,
        )

        route = chunk_router.route_chunk(chunk)

        assert isinstance(route, ChunkRoute)
        assert route.executor_class == "D3Q1"

    def test_large_number_of_chunks(self, chunk_router):
        chunks = [
            ChunkData(
                id=i,
                text=f"Chunk {i}",
                chunk_type="diagnostic" if i % 2 == 0 else "activity",
                sentences=[],
                tables=[],
                start_pos=i * 10,
                end_pos=i * 10 + 10,
                confidence=1.0,
            )
            for i in range(1000)
        ]

        execution_map = chunk_router.generate_execution_map(chunks)

        assert len(execution_map) == 1000
        assert all(isinstance(route, ChunkRoute) for route in execution_map.values())

    def test_deserialize_with_extra_fields_is_tolerant(self):
        serialized_with_extra = json.dumps(
            {
                "version": "v1",
                "extra_field": "should_be_ignored",
                "routes": {
                    "1": {
                        "chunk_id": 1,
                        "chunk_type": "diagnostic",
                        "executor_class": "D1Q1",
                        "methods": [],
                        "skip_reason": None,
                        "extra_route_field": "also_ignored",
                    }
                },
            }
        )

        execution_map = deserialize_execution_map(serialized_with_extra)

        assert len(execution_map) == 1
        assert execution_map[1].chunk_id == 1

    def test_malformed_chunk_route_in_deserialization(self):
        malformed = json.dumps(
            {
                "version": "v1",
                "routes": {
                    "1": {
                        "chunk_id": 1,
                    }
                },
            }
        )

        with pytest.raises(ValueError, match="Invalid ChunkRoute data"):
            deserialize_execution_map(malformed)


class TestCIBlockingValidation:
    """
    Critical tests that MUST pass for CI to succeed.
    These tests validate the core routing contract guarantees.
    """

    def test_ci_blocking_routing_determinism(self, chunk_router):
        chunks = [
            ChunkData(
                id=i,
                text=f"Chunk {i}",
                chunk_type=["diagnostic", "activity", "indicator"][i % 3],
                sentences=[],
                tables=[],
                start_pos=i * 10,
                end_pos=i * 10 + 10,
                confidence=0.9,
                policy_area_id=f"PA0{(i % 9) + 1}",
                dimension_id=f"DIM0{(i % 6) + 1}",
            )
            for i in range(30)
        ]

        maps = [chunk_router.generate_execution_map(chunks) for _ in range(5)]

        first_hash = compute_execution_map_hash(maps[0])
        for subsequent_map in maps[1:]:
            assert compute_execution_map_hash(subsequent_map) == first_hash

    def test_ci_blocking_serialization_roundtrip(self, chunk_router):
        chunks = [
            ChunkData(
                id=i,
                text=f"Test chunk {i}",
                chunk_type=["diagnostic", "activity", "indicator", "resource"][i % 4],
                sentences=[i],
                tables=[],
                start_pos=i * 20,
                end_pos=i * 20 + 15,
                confidence=0.85 + (i * 0.01),
                policy_area_id=f"PA0{(i % 9) + 1}",
                dimension_id=f"DIM0{(i % 6) + 1}",
            )
            for i in range(20)
        ]

        original_map = chunk_router.generate_execution_map(chunks)
        serialized = serialize_execution_map(original_map)
        restored_map = deserialize_execution_map(serialized)

        original_hash = compute_execution_map_hash(original_map)
        restored_hash = compute_execution_map_hash(restored_map)

        assert original_hash == restored_hash

    def test_ci_blocking_routing_correctness(self, chunk_router):
        test_cases = [
            ("diagnostic", "D1Q1"),
            ("activity", "D2Q1"),
            ("indicator", "D3Q1"),
            ("resource", "D1Q3"),
            ("temporal", "D1Q5"),
            ("entity", "D2Q3"),
        ]

        for chunk_type, expected_executor in test_cases:
            chunk = ChunkData(
                id=1,
                text=f"Test {chunk_type}",
                chunk_type=chunk_type,
                sentences=[],
                tables=[],
                start_pos=0,
                end_pos=10,
                confidence=1.0,
            )

            route = chunk_router.route_chunk(chunk)

            assert (
                route.executor_class == expected_executor
            ), f"Chunk type '{chunk_type}' must route to '{expected_executor}', got '{route.executor_class}'"
