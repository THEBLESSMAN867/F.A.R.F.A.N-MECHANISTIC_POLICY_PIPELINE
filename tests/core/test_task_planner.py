import json
from pathlib import Path
from typing import Any

import pytest

from farfan_pipeline.core.orchestrator.irrigation_synchronizer import (
    ChunkRoutingResult,
)
from farfan_pipeline.core.orchestrator.task_planner import (
    EXPECTED_TASKS_PER_CHUNK,
    ExecutableTask,
    MicroQuestionContext,
    _construct_task,
    _construct_task_legacy,
    _validate_cross_task,
    _validate_schema,
    extract_expected_elements,
    extract_signal_requirements,
    sort_micro_question_contexts,
)
from farfan_pipeline.core.types import ChunkData


def create_test_chunk_routing_result(
    policy_area_id: str,
    chunk_id: str,
    dimension_id: str = "DIM01",
    text_content: str = "Test chunk content",
    expected_elements: list[dict[str, Any]] | None = None,
    document_position: tuple[int, int] | None = None,
) -> ChunkRoutingResult:
    """Helper function to create test ChunkRoutingResult with all required fields."""
    if expected_elements is None:
        expected_elements = []

    # Extract PA and DIM from the provided IDs for the chunk
    target_chunk = ChunkData(
        id=0,
        text=text_content,
        chunk_type="diagnostic",
        sentences=[],
        tables=[],
        start_pos=0,
        end_pos=len(text_content),
        confidence=0.95,
        chunk_id=chunk_id,
        policy_area_id=policy_area_id,
        dimension_id=dimension_id,
    )

    return ChunkRoutingResult(
        target_chunk=target_chunk,
        chunk_id=chunk_id,
        policy_area_id=policy_area_id,
        dimension_id=dimension_id,
        text_content=text_content,
        expected_elements=expected_elements,
        document_position=document_position,
    )


class TestValidateSchema:
    def test_validate_schema_with_matching_elements(self):
        question = {
            "question_id": "Q001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "minimum": 2},
                {"type": "indicadores_cuantitativos", "minimum": 3},
            ],
        }
        chunk = {
            "id": "chunk_001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "minimum": 2},
                {"type": "indicadores_cuantitativos", "minimum": 3},
            ],
        }

        _validate_schema(question, chunk)

    def test_validate_schema_fails_on_mismatch(self):
        question = {
            "question_id": "Q001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "minimum": 2},
                {"type": "indicadores_cuantitativos", "minimum": 3},
            ],
        }
        chunk = {
            "id": "chunk_001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "minimum": 3},
                {"type": "series_temporales", "minimum": 2},
            ],
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_schema(question, chunk)

        assert "Schema mismatch" in str(exc_info.value)
        assert "fuentes_oficiales" in str(exc_info.value)
        assert "Question schema:" in str(exc_info.value)
        assert "Chunk schema:" in str(exc_info.value)

    def test_validate_schema_required_field_implication_passes_when_both_required(self):
        question = {
            "question_id": "Q001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "required": True, "minimum": 2},
                {"type": "indicadores_cuantitativos", "required": True, "minimum": 3},
            ],
        }
        chunk = {
            "id": "chunk_001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "required": True, "minimum": 2},
                {"type": "indicadores_cuantitativos", "required": True, "minimum": 3},
            ],
        }

        _validate_schema(question, chunk)

    def test_validate_schema_required_field_implication_passes_when_question_not_required(
        self,
    ):
        question = {
            "question_id": "Q001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "required": False, "minimum": 2},
                {"type": "indicadores_cuantitativos", "minimum": 3},
            ],
        }
        chunk = {
            "id": "chunk_001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "required": True, "minimum": 2},
                {"type": "indicadores_cuantitativos", "required": False, "minimum": 3},
            ],
        }

        _validate_schema(question, chunk)

    def test_validate_schema_required_field_implication_fails_when_question_required_but_chunk_not(
        self,
    ):
        question = {
            "question_id": "Q001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "required": True, "minimum": 2},
                {"type": "indicadores_cuantitativos", "required": False, "minimum": 3},
            ],
        }
        chunk = {
            "id": "chunk_001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "required": False, "minimum": 2},
                {"type": "indicadores_cuantitativos", "required": False, "minimum": 3},
            ],
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_schema(question, chunk)

        assert "Required-field implication violation" in str(exc_info.value)
        assert "Q001" in str(exc_info.value)
        assert "fuentes_oficiales" in str(exc_info.value)

    def test_validate_schema_required_field_uses_false_as_default(self):
        question = {
            "question_id": "Q001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "minimum": 2},
                {"type": "indicadores_cuantitativos", "minimum": 3},
            ],
        }
        chunk = {
            "id": "chunk_001",
            "expected_elements": [
                {"type": "fuentes_oficiales", "minimum": 2},
                {"type": "indicadores_cuantitativos", "minimum": 3},
            ],
        }

        _validate_schema(question, chunk)


class TestConstructTask:
    def test_construct_task_generates_correct_id(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 1,
            "policy_area_id": "PA01",
            "dimension_id": "DIM01",
            "base_slot": "D1-Q1",
            "cluster_id": "CL01",
            "expected_elements": [{"type": "fuentes_oficiales", "minimum": 2}],
            "signal_requirements": {"signal1": 0.3},
        }
        chunk = {"id": "chunk_001", "expected_elements": []}
        patterns = [{"type": "pattern1"}]
        signals = {"signal1": 0.5}
        generated_task_ids: set[str] = set()

        class MockRoutingResult:
            policy_area_id = "PA01"

        routing_result = MockRoutingResult()

        task = _construct_task_legacy(
            question, chunk, patterns, signals, generated_task_ids, routing_result
        )

        assert task.task_id == "MQC-001_PA01"
        assert task.question_id == "D1-Q1"
        assert task.question_global == 1
        assert task.policy_area_id == "PA01"
        assert task.dimension_id == "DIM01"
        assert task.chunk_id == "chunk_001"
        assert task.patterns == patterns
        assert task.signals == signals
        assert task.expected_elements == question["expected_elements"]
        assert task.metadata["base_slot"] == "D1-Q1"
        assert task.metadata["cluster_id"] == "CL01"
        assert "MQC-001_PA01" in generated_task_ids

    def test_construct_task_rejects_duplicate_id(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 1,
            "policy_area_id": "PA01",
            "dimension_id": "DIM01",
            "expected_elements": [],
        }
        chunk = {"id": "chunk_001", "expected_elements": []}
        patterns = []
        signals = {}
        generated_task_ids = {"MQC-001_PA01"}

        class MockRoutingResult:
            policy_area_id = "PA01"

        routing_result = MockRoutingResult()

        with pytest.raises(ValueError) as exc_info:
            _construct_task_legacy(
                question, chunk, patterns, signals, generated_task_ids, routing_result
            )

        assert "Duplicate task_id detected: MQC-001_PA01 for question D1-Q1" in str(
            exc_info.value
        )

    def test_construct_task_timestamp_format(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 15,
            "policy_area_id": "PA05",
            "dimension_id": "DIM02",
            "expected_elements": [],
        }
        chunk = {"id": "chunk_002", "expected_elements": []}
        generated_task_ids: set[str] = set()

        class MockRoutingResult:
            policy_area_id = "PA05"

        routing_result = MockRoutingResult()

        task = _construct_task_legacy(
            question, chunk, [], {}, generated_task_ids, routing_result
        )

        assert "T" in task.creation_timestamp
        assert task.creation_timestamp.endswith("Z") or "." in task.creation_timestamp


class TestValidateCrossTask:
    def test_cross_task_validation_with_canonical_questionnaire(self):
        questionnaire_path = Path(
            "system/config/questionnaire/questionnaire_monolith.json"
        )

        if not questionnaire_path.exists():
            pytest.skip("Canonical questionnaire not found")

        with open(questionnaire_path) as f:
            data = json.load(f)

        blocks = data.get("blocks", {})
        micro_questions = blocks.get("micro_questions", [])

        if not micro_questions:
            pytest.skip("No micro_questions found in questionnaire")

        plan: list[ExecutableTask] = []
        generated_ids: set[str] = set()

        chunk_map: dict[str, dict[str, Any]] = {}
        for i in range(60):
            chunk_id = f"chunk_{i:03d}"
            chunk_map[chunk_id] = {"id": chunk_id, "expected_elements": []}

        for idx, question in enumerate(micro_questions[:300]):
            chunk_id = f"chunk_{(idx // 5):03d}"

            task = ExecutableTask(
                task_id=f"MQC-{question.get('question_global', idx+1):03d}_{question.get('policy_area_id', 'PA01')}",
                question_id=question.get("question_id", f"Q{idx+1}"),
                question_global=question.get("question_global", idx + 1),
                policy_area_id=question.get("policy_area_id", "PA01"),
                dimension_id=question.get("dimension_id", "DIM01"),
                chunk_id=chunk_id,
                patterns=[],
                signals={},
                creation_timestamp="2024-01-01T00:00:00Z",
                expected_elements=[],
                metadata={},
            )
            plan.append(task)
            generated_ids.add(task.task_id)

        _validate_cross_task(plan)

        chunk_usage: dict[str, int] = {}
        for task in plan:
            chunk_usage[task.chunk_id] = chunk_usage.get(task.chunk_id, 0) + 1

        for chunk_id in chunk_map:
            if chunk_id in chunk_usage:
                assert (
                    chunk_usage[chunk_id] == EXPECTED_TASKS_PER_CHUNK
                ), f"Chunk {chunk_id} should be used exactly {EXPECTED_TASKS_PER_CHUNK} times, got {chunk_usage[chunk_id]}"

    def test_cross_task_validation_warns_on_deviations(self, caplog):
        plan = [
            ExecutableTask(
                task_id=f"MQC-{i:03d}_PA01",
                question_id=f"Q{i}",
                question_global=i,
                policy_area_id="PA01",
                dimension_id="DIM01",
                chunk_id="chunk_001",
                patterns=[],
                signals={},
                creation_timestamp="2024-01-01T00:00:00Z",
                expected_elements=[],
                metadata={},
            )
            for i in range(1, 4)
        ]

        with caplog.at_level("WARNING"):
            _validate_cross_task(plan)

        assert any(
            "Chunk usage deviation" in record.message for record in caplog.records
        )
        assert any(
            "chunk_001 used 3 times (expected 5)" in record.message
            for record in caplog.records
        )

    def test_cross_task_validation_policy_area_warning(self, caplog):
        plan = [
            ExecutableTask(
                task_id=f"MQC-{i:03d}_PA01",
                question_id=f"Q{i}",
                question_global=i,
                policy_area_id="PA01",
                dimension_id="DIM01",
                chunk_id=f"chunk_{i:03d}",
                patterns=[],
                signals={},
                creation_timestamp="2024-01-01T00:00:00Z",
                expected_elements=[],
                metadata={},
            )
            for i in range(1, 11)
        ]

        with caplog.at_level("WARNING"):
            _validate_cross_task(plan)

        assert any(
            "Policy area usage deviation" in record.message for record in caplog.records
        )
        assert any(
            "PA01 used 10 times (expected 30)" in record.message
            for record in caplog.records
        )


class TestExecutableTask:
    def test_executable_task_creation(self):
        signal_value = 0.8
        task = ExecutableTask(
            task_id="MQC-001_PA01",
            question_id="D1-Q1",
            question_global=1,
            policy_area_id="PA01",
            dimension_id="DIM01",
            chunk_id="chunk_001",
            patterns=[{"type": "pattern1"}],
            signals={"signal1": signal_value},
            creation_timestamp="2024-01-01T00:00:00Z",
            expected_elements=[{"type": "test", "minimum": 1}],
            metadata={"key": "value"},
        )

        assert task.task_id == "MQC-001_PA01"
        assert task.question_global == 1
        assert task.policy_area_id == "PA01"
        assert len(task.patterns) == 1
        assert task.signals["signal1"] == signal_value
        assert len(task.expected_elements) == 1
        assert task.metadata["key"] == "value"


class TestMicroQuestionContext:
    def test_context_is_frozen(self):
        context = MicroQuestionContext(
            task_id="MQC-001_PA01",
            question_id="D1-Q1",
            question_global=1,
            policy_area_id="PA01",
            dimension_id="DIM01",
            chunk_id="chunk_001",
            base_slot="D1-Q1",
            cluster_id="CL01",
            patterns=[{"type": "pattern1"}],
            signals={"signal1": 0.5},
            expected_elements=[{"type": "test", "minimum": 1}],
            signal_requirements={"signal1": 0.3},
            creation_timestamp="2024-01-01T00:00:00Z",
        )

        assert context.task_id == "MQC-001_PA01"
        assert context.question_global == 1
        assert isinstance(context.patterns, tuple)
        assert isinstance(context.expected_elements, tuple)

        with pytest.raises(AttributeError):
            context.task_id = "new_id"

    def test_extract_expected_elements(self):
        context = MicroQuestionContext(
            task_id="MQC-001_PA01",
            question_id="D1-Q1",
            question_global=1,
            policy_area_id="PA01",
            dimension_id="DIM01",
            chunk_id="chunk_001",
            base_slot="D1-Q1",
            cluster_id="CL01",
            patterns=[],
            signals={},
            expected_elements=[{"type": "test", "minimum": 1}, {"type": "test2"}],
            signal_requirements={},
            creation_timestamp="2024-01-01T00:00:00Z",
        )

        elements = extract_expected_elements(context)
        assert isinstance(elements, list)
        assert len(elements) == 2
        assert elements[0]["type"] == "test"

    def test_extract_signal_requirements(self):
        context = MicroQuestionContext(
            task_id="MQC-001_PA01",
            question_id="D1-Q1",
            question_global=1,
            policy_area_id="PA01",
            dimension_id="DIM01",
            chunk_id="chunk_001",
            base_slot="D1-Q1",
            cluster_id="CL01",
            patterns=[],
            signals={},
            expected_elements=[],
            signal_requirements={"signal1": 0.5, "signal2": 0.7},
            creation_timestamp="2024-01-01T00:00:00Z",
        )

        requirements = extract_signal_requirements(context)
        assert isinstance(requirements, dict)
        assert requirements["signal1"] == 0.5
        assert requirements["signal2"] == 0.7

    def test_sort_micro_question_contexts(self):
        contexts = [
            MicroQuestionContext(
                task_id="MQC-002_PA02",
                question_id="D1-Q2",
                question_global=2,
                policy_area_id="PA02",
                dimension_id="DIM01",
                chunk_id="chunk_002",
                base_slot="D1-Q2",
                cluster_id="CL01",
                patterns=[],
                signals={},
                expected_elements=[],
                signal_requirements={},
                creation_timestamp="2024-01-01T00:00:00Z",
            ),
            MicroQuestionContext(
                task_id="MQC-051_PA01",
                question_id="D2-Q1",
                question_global=51,
                policy_area_id="PA01",
                dimension_id="DIM02",
                chunk_id="chunk_010",
                base_slot="D2-Q1",
                cluster_id="CL01",
                patterns=[],
                signals={},
                expected_elements=[],
                signal_requirements={},
                creation_timestamp="2024-01-01T00:00:00Z",
            ),
            MicroQuestionContext(
                task_id="MQC-001_PA01",
                question_id="D1-Q1",
                question_global=1,
                policy_area_id="PA01",
                dimension_id="DIM01",
                chunk_id="chunk_001",
                base_slot="D1-Q1",
                cluster_id="CL01",
                patterns=[],
                signals={},
                expected_elements=[],
                signal_requirements={},
                creation_timestamp="2024-01-01T00:00:00Z",
            ),
        ]

        sorted_contexts = sort_micro_question_contexts(contexts)
        assert sorted_contexts[0].question_global == 1
        assert sorted_contexts[1].question_global == 2
        assert sorted_contexts[2].question_global == 51
        assert sorted_contexts[0].dimension_id == "DIM01"
        assert sorted_contexts[2].dimension_id == "DIM02"


class TestConstructTaskNew:
    def test_construct_task_with_valid_inputs(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 42,
            "dimension_id": "DIM01",
            "base_slot": "D1-Q1",
            "cluster_id": "CL01",
            "expected_elements": [{"type": "test", "minimum": 1}],
            "signal_requirements": {"signal1": 0.3},
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA05", chunk_id="PA05-DIM01", dimension_id="DIM01"
        )
        applicable_patterns = ({"pattern": "p1"}, {"pattern": "p2"})
        resolved_signals = (0.8, 0.9, 0.7)
        generated_task_ids: set[str] = set()
        correlation_id = "corr-123-abc"

        task = _construct_task(
            question,
            routing_result,
            applicable_patterns,
            resolved_signals,
            generated_task_ids,
            correlation_id,
        )

        assert task.task_id == "MQC-042_PA05"
        assert task.question_id == "D1-Q1"
        assert task.question_global == 42
        assert task.policy_area_id == "PA05"
        assert task.dimension_id == "DIM01"
        assert task.chunk_id == "PA05-DIM01"
        assert len(task.patterns) == 2
        assert task.metadata["correlation_id"] == correlation_id
        assert task.metadata["base_slot"] == "D1-Q1"
        assert task.metadata["cluster_id"] == "CL01"
        assert "MQC-042_PA05" in generated_task_ids

    def test_construct_task_missing_question_global(self):
        question = {
            "question_id": "D1-Q1",
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        with pytest.raises(ValueError) as exc_info:
            _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

        assert "Task construction failure for D1-Q1" in str(exc_info.value)
        assert "question_global field missing or None" in str(exc_info.value)

    def test_construct_task_missing_question_global_unknown_id(self):
        question = {
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        with pytest.raises(ValueError) as exc_info:
            _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

        assert "Task construction failure for UNKNOWN" in str(exc_info.value)
        assert "question_global field missing or None" in str(exc_info.value)

    def test_construct_task_question_global_not_integer(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": "42",
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        with pytest.raises(ValueError) as exc_info:
            _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

        assert "Task construction failure for D1-Q1" in str(exc_info.value)
        assert "question_global must be an integer" in str(exc_info.value)
        assert "got str" in str(exc_info.value)

    def test_construct_task_question_global_below_range(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": -1,
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        with pytest.raises(ValueError) as exc_info:
            _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

        assert "Task construction failure for D1-Q1" in str(exc_info.value)
        assert "question_global must be in range 0-999" in str(exc_info.value)
        assert "got -1" in str(exc_info.value)

    def test_construct_task_question_global_above_range(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 1000,
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        with pytest.raises(ValueError) as exc_info:
            _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

        assert "Task construction failure for D1-Q1" in str(exc_info.value)
        assert "question_global must be in range 0-999" in str(exc_info.value)
        assert "got 1000" in str(exc_info.value)

    def test_construct_task_duplicate_task_id(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 42,
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA05", chunk_id="PA05-DIM01", dimension_id="DIM01"
        )
        generated_task_ids = {"MQC-042_PA05"}

        with pytest.raises(ValueError) as exc_info:
            _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

        assert "Duplicate task_id detected: MQC-042_PA05" in str(exc_info.value)

    def test_construct_task_reserves_id_before_completion(self):
        question = {
            "question_id": "D1-Q1",
            "question_global": 42,
            "dimension_id": "DIM01",
        }
        routing_result = create_test_chunk_routing_result(
            policy_area_id="PA05", chunk_id="PA05-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        task = _construct_task(
            question, routing_result, (), (), generated_task_ids, "corr-123"
        )

        assert "MQC-042_PA05" in generated_task_ids
        assert task.task_id == "MQC-042_PA05"

    def test_construct_task_boundary_values(self):
        question_min = {
            "question_id": "D1-Q1",
            "question_global": 0,
            "dimension_id": "DIM01",
        }
        routing_result_min = create_test_chunk_routing_result(
            policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
        )
        generated_task_ids: set[str] = set()

        task_min = _construct_task(
            question_min, routing_result_min, (), (), generated_task_ids, "corr-123"
        )

        assert task_min.task_id == "MQC-000_PA01"
        assert task_min.question_global == 0

        question_max = {
            "question_id": "D6-Q50",
            "question_global": 999,
            "dimension_id": "DIM06",
        }
        routing_result_max = create_test_chunk_routing_result(
            policy_area_id="PA10", chunk_id="PA10-DIM06", dimension_id="DIM06"
        )

        task_max = _construct_task(
            question_max, routing_result_max, (), (), generated_task_ids, "corr-456"
        )

        assert task_max.task_id == "MQC-999_PA10"
        assert task_max.question_global == 999

    def test_construct_task_formats_task_id_with_leading_zeros(self):
        test_cases = [
            (1, "MQC-001_PA01"),
            (10, "MQC-010_PA01"),
            (100, "MQC-100_PA01"),
            (999, "MQC-999_PA01"),
        ]

        for question_global, expected_id in test_cases:
            question = {
                "question_id": f"Q{question_global}",
                "question_global": question_global,
                "dimension_id": "DIM01",
            }
            routing_result = create_test_chunk_routing_result(
                policy_area_id="PA01", chunk_id="PA01-DIM01", dimension_id="DIM01"
            )
            generated_task_ids: set[str] = set()

            task = _construct_task(
                question, routing_result, (), (), generated_task_ids, "corr-123"
            )

            assert task.task_id == expected_id
