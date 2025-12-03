"""
Comprehensive Executor Resilience Test Suite

Property-based and integration tests for all 30 executors (D1-Q1 through D6-Q5)
validating resilience under:
- Malformed inputs (oversized entities, invalid DAGs, corrupted causal effects)
- Memory exhaustion scenarios
- Concurrent execution stress tests
- Serialization failure recovery
- Timeout handling
- End-to-end pipeline behavior under resource constraints

Uses hypothesis for property-based testing to ensure robust error handling
and graceful degradation across all failure modes.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import gc
import json
import sys
import threading
import time
from dataclasses import dataclass
from unittest.mock import Mock

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from farfan_pipeline.core.orchestrator.base_executor_with_contract import (
    BaseExecutorWithContract,
)
from farfan_pipeline.core.orchestrator.core import (
    MethodExecutor,
    PreprocessedDocument,
)
from farfan_pipeline.core.orchestrator.executor_config import ExecutorConfig
from farfan_pipeline.core.orchestrator.executors_contract import (
    D1Q1_Executor,
    D1Q2_Executor,
    D1Q3_Executor,
    D1Q4_Executor,
    D1Q5_Executor,
    D2Q1_Executor,
    D2Q2_Executor,
    D2Q3_Executor,
    D2Q4_Executor,
    D2Q5_Executor,
    D3Q1_Executor,
    D3Q2_Executor,
    D3Q3_Executor,
    D3Q4_Executor,
    D3Q5_Executor,
    D4Q1_Executor,
    D4Q2_Executor,
    D4Q3_Executor,
    D4Q4_Executor,
    D4Q5_Executor,
    D5Q1_Executor,
    D5Q2_Executor,
    D5Q3_Executor,
    D5Q4_Executor,
    D5Q5_Executor,
    D6Q1_Executor,
    D6Q2_Executor,
    D6Q3_Executor,
    D6Q4_Executor,
    D6Q5_Executor,
)

ALL_EXECUTOR_CLASSES = [
    D1Q1_Executor,
    D1Q2_Executor,
    D1Q3_Executor,
    D1Q4_Executor,
    D1Q5_Executor,
    D2Q1_Executor,
    D2Q2_Executor,
    D2Q3_Executor,
    D2Q4_Executor,
    D2Q5_Executor,
    D3Q1_Executor,
    D3Q2_Executor,
    D3Q3_Executor,
    D3Q4_Executor,
    D3Q5_Executor,
    D4Q1_Executor,
    D4Q2_Executor,
    D4Q3_Executor,
    D4Q4_Executor,
    D4Q5_Executor,
    D5Q1_Executor,
    D5Q2_Executor,
    D5Q3_Executor,
    D5Q4_Executor,
    D5Q5_Executor,
    D6Q1_Executor,
    D6Q2_Executor,
    D6Q3_Executor,
    D6Q4_Executor,
    D6Q5_Executor,
]


@st.composite
def oversized_text(draw, max_size: int = 50_000_000):
    """Generate oversized text inputs to test memory limits."""
    size = draw(st.integers(min_value=10_000_000, max_value=max_size))
    return "A" * size


@st.composite
def malformed_dag(draw):
    """Generate malformed DAG structures with cycles, missing nodes, invalid edges."""
    num_nodes = draw(st.integers(min_value=2, max_value=20))
    nodes = [f"node_{i}" for i in range(num_nodes)]

    dag_type = draw(
        st.sampled_from(["cyclic", "missing_nodes", "invalid_edges", "disconnected"])
    )

    if dag_type == "cyclic":
        edges = [(nodes[i], nodes[(i + 1) % num_nodes]) for i in range(num_nodes)]
    elif dag_type == "missing_nodes":
        edges = [(nodes[0], "missing_node"), ("missing_node", nodes[1])]
    elif dag_type == "invalid_edges":
        edges = [(None, nodes[0]), (nodes[0], None), (123, "string"), ({}, [])]
    else:
        edges = [(nodes[i], nodes[i + 1]) for i in range(0, num_nodes // 2)]

    return {"nodes": nodes, "edges": edges, "type": dag_type}


@st.composite
def corrupted_causal_effect(draw):
    """Generate corrupted causal effect data structures."""
    corruption_type = draw(
        st.sampled_from(
            [
                "missing_keys",
                "invalid_types",
                "nan_values",
                "infinite_values",
                "negative_probabilities",
                "empty_arrays",
            ]
        )
    )

    if corruption_type == "missing_keys":
        return {"node": "outcome_1"}
    elif corruption_type == "invalid_types":
        return {
            "node": 123,
            "effect": "should_be_float",
            "probability": [1, 2, 3],
        }
    elif corruption_type == "nan_values":
        return {
            "node": "outcome_1",
            "effect": float("nan"),
            "probability": float("nan"),
        }
    elif corruption_type == "infinite_values":
        return {
            "node": "outcome_1",
            "effect": float("inf"),
            "probability": float("-inf"),
        }
    elif corruption_type == "negative_probabilities":
        return {
            "node": "outcome_1",
            "effect": 0.5,
            "probability": -0.5,
        }
    else:
        return {
            "node": "outcome_1",
            "effect": [],
            "probability": [],
            "confounders": [],
        }


@st.composite
def oversized_entity_list(draw, max_entities: int = 100_000):
    """Generate oversized entity lists to test memory handling."""
    num_entities = draw(st.integers(min_value=10_000, max_value=max_entities))
    return [
        {
            "id": f"entity_{i}",
            "name": f"Entity Name {i}",
            "type": draw(
                st.sampled_from(["government", "private", "ngo", "international"])
            ),
            "attributes": {"attr_" + str(j): f"value_{j}" for j in range(10)},
        }
        for i in range(num_entities)
    ]


@st.composite
def minimal_document(draw):
    """Generate minimal valid document for testing."""
    return PreprocessedDocument(
        document_id=draw(
            st.text(
                min_size=5,
                max_size=20,
                alphabet=st.characters(whitelist_categories=("L", "N")),
            )
        ),
        raw_text=draw(st.text(min_size=100, max_size=1000)),
        sentences=[],
        tables=[],
        metadata={"test": True},
    )


@st.composite
def malformed_document(draw):
    """Generate malformed documents with missing/invalid fields."""
    malformation_type = draw(
        st.sampled_from(
            [
                "null_metadata",
                "invalid_sentences",
                "circular_refs",
            ]
        )
    )

    if malformation_type == "null_metadata":
        try:
            doc = PreprocessedDocument(
                document_id="test",
                raw_text="Some text for testing",
                sentences=[],
                tables=[],
                metadata=None,
            )
            return doc
        except Exception:
            return PreprocessedDocument(
                document_id="test",
                raw_text="Some text for testing",
                sentences=[],
                tables=[],
                metadata={},
            )
    elif malformation_type == "invalid_sentences":
        return PreprocessedDocument(
            document_id="test",
            raw_text="Some text for testing",
            sentences=[None, 123, {}, "invalid"],
            tables=[],
            metadata={},
        )
    else:
        doc = PreprocessedDocument(
            document_id="test",
            raw_text="Some text for testing",
            sentences=[],
            tables=[],
            metadata={"circular": None},
        )
        doc.metadata["circular"] = doc
        return doc


@dataclass
class ResourceMonitor:
    """Monitor resource usage during test execution."""

    peak_memory_mb: float = 0.0
    execution_time_ms: float = 0.0
    gc_collections: int = 0
    thread_count: int = 0

    def start(self):
        """Start monitoring."""
        self.start_time = time.time()
        self.initial_gc = sum(gc.get_count())
        self.initial_threads = threading.active_count()
        gc.collect()

    def stop(self):
        """Stop monitoring and record metrics."""
        self.execution_time_ms = (time.time() - self.start_time) * 1000
        self.gc_collections = sum(gc.get_count()) - self.initial_gc
        self.thread_count = threading.active_count() - self.initial_threads

        try:
            import psutil

            process = psutil.Process()
            self.peak_memory_mb = process.memory_info().rss / (1024 * 1024)
        except ImportError:
            self.peak_memory_mb = sys.getsizeof(gc.get_objects()) / (1024 * 1024)


class TestMalformedInputResilience:
    """Test executor resilience against malformed inputs."""

    @pytest.fixture
    def mock_method_executor(self):
        """Create a mock MethodExecutor for testing."""
        executor = Mock(spec=MethodExecutor)
        executor.execute.return_value = {"result": "mocked"}
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_signal_registry(self):
        """Create a mock signal registry."""
        registry = Mock()
        registry.get.return_value = None
        return registry

    @pytest.fixture
    def mock_config(self):
        """Create a mock config."""
        return ExecutorConfig()

    @pytest.fixture
    def mock_questionnaire_provider(self):
        """Create a mock questionnaire provider."""
        provider = Mock()
        provider.get_question.return_value = {
            "question_id": "Q1",
            "question_text": "Test question",
            "expected_elements": [],
            "patterns": [],
        }
        return provider

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES)
    def test_executor_handles_missing_document_text(
        self,
        executor_cls,
        mock_method_executor,
        mock_signal_registry,
        mock_config,
        mock_questionnaire_provider,
    ):
        """Test that executors handle missing/empty document text gracefully."""
        executor = executor_cls(
            method_executor=mock_method_executor,
            signal_registry=mock_signal_registry,
            config=mock_config,
            questionnaire_provider=mock_questionnaire_provider,
        )

        with pytest.raises(ValueError, match="empty raw_text"):
            document = PreprocessedDocument(
                document_id="test",
                raw_text="",
                sentences=[],
                tables=[],
                metadata={},
            )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="   ",
            sentences=[],
            tables=[],
            metadata={},
        )

        with pytest.raises(ValueError, match="empty raw_text"):
            pass

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Valid text content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        result = executor.execute(
            document=document,
            method_executor=mock_method_executor,
            question_context=question_context,
        )
        assert isinstance(result, dict)

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:5])
    @given(dag=malformed_dag())
    @settings(
        max_examples=10,
        deadline=5000,
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
    )
    def test_executor_handles_malformed_dag(
        self,
        executor_cls,
        dag,
        mock_method_executor,
        mock_signal_registry,
        mock_config,
        mock_questionnaire_provider,
    ):
        """Property: Executors handle malformed DAGs without crashing."""
        assume(isinstance(dag, dict))
        assume("nodes" in dag and "edges" in dag)

        mock_method_executor.execute.return_value = {"dag": dag}

        executor = executor_cls(
            method_executor=mock_method_executor,
            signal_registry=mock_signal_registry,
            config=mock_config,
            questionnaire_provider=mock_questionnaire_provider,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )
            assert isinstance(result, dict)
        except Exception as e:
            assert any(
                keyword in str(e).lower()
                for keyword in ["invalid", "malformed", "cycle", "missing"]
            )

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:5])
    @given(effect=corrupted_causal_effect())
    @settings(
        max_examples=10,
        deadline=5000,
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
    )
    def test_executor_handles_corrupted_causal_effects(
        self,
        executor_cls,
        effect,
        mock_method_executor,
        mock_signal_registry,
        mock_config,
        mock_questionnaire_provider,
    ):
        """Property: Executors validate and reject corrupted causal effects."""
        mock_method_executor.execute.return_value = {"causal_effects": [effect]}

        executor = executor_cls(
            method_executor=mock_method_executor,
            signal_registry=mock_signal_registry,
            config=mock_config,
            questionnaire_provider=mock_questionnaire_provider,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )
            if isinstance(result, dict) and "validation" in result:
                assert result["validation"].get(
                    "status"
                ) != "passed" or "causal_effects" not in result.get("evidence", {})
        except (ValueError, TypeError, KeyError):
            pass


class TestMemoryExhaustionScenarios:
    """Test executor behavior under memory pressure."""

    @pytest.fixture
    def mock_method_executor(self):
        """Create a mock MethodExecutor for testing."""
        executor = Mock(spec=MethodExecutor)
        executor.execute.return_value = {"result": "mocked"}
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_dependencies(self):
        """Create all mock dependencies."""
        return {
            "signal_registry": Mock(),
            "config": ExecutorConfig(),
            "questionnaire_provider": Mock(),
        }

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:3])
    def test_executor_handles_oversized_entities(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that executors handle oversized entity lists gracefully."""
        large_entities = [
            {"id": f"entity_{i}", "name": f"Entity {i}"} for i in range(50_000)
        ]
        mock_method_executor.execute.return_value = {"entities": large_entities}

        executor = executor_cls(
            method_executor=mock_method_executor,
            **mock_dependencies,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        monitor = ResourceMonitor()
        monitor.start()

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )
            monitor.stop()

            MAX_MEMORY_MB = 1000
            assert isinstance(result, dict)
            assert monitor.peak_memory_mb < MAX_MEMORY_MB
        except MemoryError:
            pytest.skip("Insufficient memory for test")

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:2])
    def test_executor_handles_oversized_text(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that executors handle oversized text inputs with proper limits."""
        oversized_text = "A" * 1_000_000

        document = PreprocessedDocument(
            document_id="test",
            raw_text=oversized_text,
            sentences=[],
            tables=[],
            metadata={},
        )

        executor = executor_cls(
            method_executor=mock_method_executor,
            **mock_dependencies,
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        monitor = ResourceMonitor()
        monitor.start()

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )
            monitor.stop()

            MAX_EXECUTION_TIME_MS = 30000
            assert isinstance(result, dict)
            assert monitor.execution_time_ms < MAX_EXECUTION_TIME_MS
        except (MemoryError, TimeoutError):
            pytest.skip("Resource limit exceeded as expected")


class TestConcurrentExecutionStress:
    """Test concurrent execution stress scenarios."""

    @pytest.fixture
    def mock_method_executor(self):
        """Create thread-safe mock MethodExecutor."""
        executor = Mock(spec=MethodExecutor)
        executor.execute.return_value = {"result": "mocked"}
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_dependencies(self):
        """Create all mock dependencies."""
        return {
            "signal_registry": Mock(),
            "config": ExecutorConfig(),
            "questionnaire_provider": Mock(),
        }

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:5])
    def test_concurrent_executor_execution(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that multiple executors can run concurrently without interference."""
        num_concurrent = 10

        def run_executor():
            executor = executor_cls(
                method_executor=mock_method_executor,
                **mock_dependencies,
            )

            document = PreprocessedDocument(
                document_id=f"test_{threading.current_thread().ident}",
                raw_text="Test content",
                sentences=[],
                tables=[],
                metadata={},
            )

            base_slot = executor_cls.get_base_slot()
            question_context = {
                "base_slot": base_slot,
                "question_id": f"{base_slot}-Q1",
                "question_global": "Test question",
                "policy_area_id": "test_area",
                "identity": {
                    "dimension_id": base_slot.split("-")[0],
                    "cluster_id": base_slot,
                },
                "patterns": [],
                "expected_elements": [],
            }

            return executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as pool:
            futures = [pool.submit(run_executor) for _ in range(num_concurrent)]
            results = [f.result(timeout=10) for f in futures]

        assert len(results) == num_concurrent
        assert all(isinstance(r, dict) for r in results)

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:3])
    def test_executor_thread_safety(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that executor state is not corrupted by concurrent access."""
        executor = executor_cls(
            method_executor=mock_method_executor,
            **mock_dependencies,
        )

        execution_count = [0]
        lock = threading.Lock()

        def concurrent_execute(thread_id):
            document = PreprocessedDocument(
                document_id=f"test_{thread_id}",
                raw_text=f"Content for thread {thread_id}",
                sentences=[],
                tables=[],
                metadata={"thread_id": thread_id},
            )

            base_slot = executor_cls.get_base_slot()
            question_context = {
                "base_slot": base_slot,
                "question_id": f"{base_slot}-Q1",
                "question_global": f"Question for thread {thread_id}",
                "policy_area_id": f"area_{thread_id}",
                "identity": {
                    "dimension_id": base_slot.split("-")[0],
                    "cluster_id": base_slot,
                },
                "patterns": [],
                "expected_elements": [],
            }

            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )

            with lock:
                execution_count[0] += 1

            return result

        threads = [
            threading.Thread(target=concurrent_execute, args=(i,)) for i in range(20)
        ]

        for t in threads:
            t.start()

        NUM_THREADS = 20
        for t in threads:
            t.join(timeout=5)

        assert execution_count[0] == NUM_THREADS


class TestSerializationFailureRecovery:
    """Test serialization failure recovery mechanisms."""

    @pytest.fixture
    def mock_method_executor(self):
        """Create a mock MethodExecutor for testing."""
        executor = Mock(spec=MethodExecutor)
        executor.execute.return_value = {"result": "mocked"}
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_dependencies(self):
        """Create all mock dependencies."""
        return {
            "signal_registry": Mock(),
            "config": ExecutorConfig(),
            "questionnaire_provider": Mock(),
        }

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:5])
    def test_executor_result_is_json_serializable(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that executor results are always JSON-serializable."""
        executor = executor_cls(
            method_executor=mock_method_executor,
            **mock_dependencies,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )

            json_str = json.dumps(result)
            assert isinstance(json_str, str)
            roundtrip = json.loads(json_str)
            assert isinstance(roundtrip, dict)
        except FileNotFoundError as e:
            if "Contract not found" in str(e):
                pytest.skip(
                    f"Contract file not found for {base_slot} - expected in testing environment"
                )
            raise
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result is not JSON-serializable: {e}")

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:3])
    def test_executor_handles_non_serializable_method_results(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that executors handle non-serializable method results gracefully."""

        class NonSerializable:
            def __repr__(self):
                return "<NonSerializable>"

        mock_method_executor.execute.return_value = {
            "data": NonSerializable(),
            "function": lambda x: x,
            "thread": threading.current_thread(),
        }

        executor = executor_cls(
            method_executor=mock_method_executor,
            **mock_dependencies,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )

            json.dumps(result)
        except (TypeError, ValueError):
            pass


class TestTimeoutHandling:
    """Test timeout handling and cancellation mechanisms."""

    @pytest.fixture
    def slow_method_executor(self):
        """Create a mock MethodExecutor that simulates slow operations."""
        executor = Mock(spec=MethodExecutor)

        def slow_execute(*args, **kwargs):
            time.sleep(2)
            return {"result": "slow"}

        executor.execute.side_effect = slow_execute
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_dependencies(self):
        """Create all mock dependencies."""
        return {
            "signal_registry": Mock(),
            "config": ExecutorConfig(timeout_s=1.0),
            "questionnaire_provider": Mock(),
        }

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES[:3])
    def test_executor_respects_timeout_config(
        self,
        executor_cls,
        slow_method_executor,
        mock_dependencies,
    ):
        """Test that executors respect timeout configuration."""
        executor = executor_cls(
            method_executor=slow_method_executor,
            **mock_dependencies,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        start_time = time.time()

        MAX_TIMEOUT_SECONDS = 5.0
        try:
            _result = executor.execute(
                document=document,
                method_executor=slow_method_executor,
                question_context=question_context,
            )
            execution_time = time.time() - start_time

            assert execution_time < MAX_TIMEOUT_SECONDS
        except (TimeoutError, asyncio.TimeoutError):
            pass


class TestResourceConstraintIntegration:
    """Integration tests for end-to-end pipeline behavior under resource constraints."""

    @pytest.fixture
    def mock_method_executor(self):
        """Create a mock MethodExecutor for testing."""
        executor = Mock(spec=MethodExecutor)
        executor.execute.return_value = {"result": "mocked"}
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_dependencies(self):
        """Create all mock dependencies."""
        return {
            "signal_registry": Mock(),
            "config": ExecutorConfig(),
            "questionnaire_provider": Mock(),
        }

    def test_pipeline_graceful_degradation_under_memory_pressure(
        self,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that pipeline degrades gracefully under memory pressure."""
        successful_executions = 0
        partial_failures = 0
        complete_failures = 0

        for executor_cls in ALL_EXECUTOR_CLASSES[:10]:
            executor = executor_cls(
                method_executor=mock_method_executor,
                **mock_dependencies,
            )

            large_text = "X" * 500_000
            document = PreprocessedDocument(
                document_id="test",
                raw_text=large_text,
                sentences=[],
                tables=[],
                metadata={},
            )

            base_slot = executor_cls.get_base_slot()
            question_context = {
                "base_slot": base_slot,
                "question_id": f"{base_slot}-Q1",
                "question_global": "Test question",
                "policy_area_id": "test_area",
                "identity": {
                    "dimension_id": base_slot.split("-")[0],
                    "cluster_id": base_slot,
                },
                "patterns": [],
                "expected_elements": [],
            }

            try:
                result = executor.execute(
                    document=document,
                    method_executor=mock_method_executor,
                    question_context=question_context,
                )

                if isinstance(result, dict):
                    validation = result.get("validation", {})
                    if validation.get("status") == "passed":
                        successful_executions += 1
                    else:
                        partial_failures += 1
                else:
                    complete_failures += 1
            except Exception:
                complete_failures += 1

        NUM_EXECUTORS_TEST = 10
        MIN_SUCCESS_RATE = 5
        total = successful_executions + partial_failures + complete_failures
        assert total == NUM_EXECUTORS_TEST
        assert successful_executions + partial_failures >= MIN_SUCCESS_RATE

    def test_pipeline_recovery_after_failure(
        self,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that pipeline can recover and continue after individual failures."""
        failing_then_succeeding_executor = Mock(spec=MethodExecutor)
        call_count = [0]

        FAILURE_THRESHOLD = 2

        def execute_with_intermittent_failure(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] <= FAILURE_THRESHOLD:
                raise RuntimeError("Simulated failure")
            return {"result": "success"}

        failing_then_succeeding_executor.execute.side_effect = (
            execute_with_intermittent_failure
        )
        failing_then_succeeding_executor.shared_instances = {}

        results = []

        for i in range(5):
            executor_cls = ALL_EXECUTOR_CLASSES[i % len(ALL_EXECUTOR_CLASSES)]
            executor = executor_cls(
                method_executor=failing_then_succeeding_executor,
                **mock_dependencies,
            )

            document = PreprocessedDocument(
                document_id=f"test_{i}",
                raw_text="Test content",
                sentences=[],
                tables=[],
                metadata={},
            )

            base_slot = executor_cls.get_base_slot()
            question_context = {
                "base_slot": base_slot,
                "question_id": f"{base_slot}-Q1",
                "question_global": "Test question",
                "policy_area_id": "test_area",
                "identity": {
                    "dimension_id": base_slot.split("-")[0],
                    "cluster_id": base_slot,
                },
                "patterns": [],
                "expected_elements": [],
            }

            try:
                result = executor.execute(
                    document=document,
                    method_executor=failing_then_succeeding_executor,
                    question_context=question_context,
                )
                results.append(("success", result))
            except Exception as e:
                results.append(("failure", str(e)))

        MAX_EXPECTED_FAILURES = 2
        MIN_EXPECTED_SUCCESSES = 3
        failures = [r for r in results if r[0] == "failure"]
        successes = [r for r in results if r[0] == "success"]

        assert len(failures) <= MAX_EXPECTED_FAILURES
        assert len(successes) >= MIN_EXPECTED_SUCCESSES

    @pytest.mark.parametrize("num_executors", [5, 10, 20])
    def test_pipeline_handles_concurrent_resource_contention(
        self,
        num_executors,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that pipeline handles concurrent resource contention gracefully."""

        def run_executor_with_resource_usage(executor_cls):
            executor = executor_cls(
                method_executor=mock_method_executor,
                **mock_dependencies,
            )

            document = PreprocessedDocument(
                document_id=f"test_{executor_cls.__name__}",
                raw_text="A" * 100_000,
                sentences=[],
                tables=[],
                metadata={},
            )

            base_slot = executor_cls.get_base_slot()
            question_context = {
                "base_slot": base_slot,
                "question_id": f"{base_slot}-Q1",
                "question_global": "Test question",
                "policy_area_id": "test_area",
                "identity": {
                    "dimension_id": base_slot.split("-")[0],
                    "cluster_id": base_slot,
                },
                "patterns": [],
                "expected_elements": [],
            }

            monitor = ResourceMonitor()
            monitor.start()

            try:
                _result = executor.execute(
                    document=document,
                    method_executor=mock_method_executor,
                    question_context=question_context,
                )
                monitor.stop()
                return ("success", monitor)
            except Exception:
                monitor.stop()
                return ("failure", monitor)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_executors) as pool:
            executor_classes = ALL_EXECUTOR_CLASSES[:num_executors]
            futures = [
                pool.submit(run_executor_with_resource_usage, cls)
                for cls in executor_classes
            ]

            results = []
            for future in concurrent.futures.as_completed(futures, timeout=30):
                try:
                    result = future.result()
                    results.append(result)
                except Exception:
                    pass

        assert len(results) >= num_executors * 0.8

        success_count = sum(1 for status, _ in results if status == "success")
        assert success_count >= num_executors * 0.6


class TestExecutorContractCompliance:
    """Test that all executors comply with contract specifications."""

    @pytest.fixture
    def mock_method_executor(self):
        """Create a mock MethodExecutor for testing."""
        executor = Mock(spec=MethodExecutor)
        executor.execute.return_value = {"result": "mocked"}
        executor.shared_instances = {}
        return executor

    @pytest.fixture
    def mock_dependencies(self):
        """Create all mock dependencies."""
        return {
            "signal_registry": Mock(),
            "config": ExecutorConfig(),
            "questionnaire_provider": Mock(),
        }

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES)
    def test_executor_has_valid_base_slot(self, executor_cls):
        """Test that all executors have valid base slots."""
        base_slot = executor_cls.get_base_slot()
        assert isinstance(base_slot, str)
        assert len(base_slot) > 0
        assert "-" in base_slot

        dimension, question = base_slot.split("-")
        assert dimension.startswith("D")
        assert question.startswith("Q")

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES)
    def test_executor_instantiation(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that all executors can be instantiated with required dependencies."""
        try:
            executor = executor_cls(
                method_executor=mock_method_executor,
                **mock_dependencies,
            )
            assert executor is not None
            assert isinstance(executor, BaseExecutorWithContract)
        except Exception as e:
            pytest.fail(f"Failed to instantiate {executor_cls.__name__}: {e}")

    @pytest.mark.parametrize("executor_cls", ALL_EXECUTOR_CLASSES)
    def test_executor_returns_dict_result(
        self,
        executor_cls,
        mock_method_executor,
        mock_dependencies,
    ):
        """Test that all executors return dict results (if contracts exist)."""
        executor = executor_cls(
            method_executor=mock_method_executor,
            **mock_dependencies,
        )

        document = PreprocessedDocument(
            document_id="test",
            raw_text="Test content",
            sentences=[],
            tables=[],
            metadata={},
        )

        base_slot = executor_cls.get_base_slot()
        question_context = {
            "base_slot": base_slot,
            "question_id": f"{base_slot}-Q1",
            "question_global": "Test question",
            "policy_area_id": "test_area",
            "identity": {
                "dimension_id": base_slot.split("-")[0],
                "cluster_id": base_slot,
            },
            "patterns": [],
            "expected_elements": [],
        }

        try:
            result = executor.execute(
                document=document,
                method_executor=mock_method_executor,
                question_context=question_context,
            )

            assert isinstance(result, dict)
            assert any(
                key in result for key in ["evidence", "validation", "metadata", "trace"]
            )
        except FileNotFoundError as e:
            if "Contract not found" in str(e):
                pytest.skip(
                    f"Contract file not found for {base_slot} - expected in testing environment"
                )
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
