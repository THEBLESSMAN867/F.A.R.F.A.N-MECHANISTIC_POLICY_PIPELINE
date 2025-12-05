"""
Factory module — canonical Dependency Injection (DI) and access control for F.A.R.F.A.N.

This module is the single authoritative boundary for:
- Canonical monolith access (CanonicalQuestionnaire)
- Signal registry construction and enrichment
- Method injection via MethodExecutor
- Orchestrator construction with strict DI

Design Principles (Factory Pattern + DI):
- Orchestrator and Executors never touch I/O nor load the monolith directly.
- Factory loads and validates the canonical questionnaire exactly once.
- Factory constructs signal registries and enriched packs centrally.
- Factory wires MethodExecutor with registries and special instantiation rules.

Scope:
- Infrastructure layer only. No business logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional

from farfan_pipeline.core.orchestrator.core import Orchestrator, MethodExecutor
from farfan_pipeline.core.orchestrator.executor_config import ExecutorConfig
from farfan_pipeline.core.orchestrator.method_registry import MethodRegistry, setup_default_instantiation_rules
from farfan_pipeline.core.orchestrator.signal_registry import (
	QuestionnaireSignalRegistry,
	create_signal_registry as _create_signal_registry,  # factory function v2.0
)
from farfan_pipeline.core.orchestrator.signal_intelligence_layer import (
	create_enriched_signal_pack,
)
from farfan_pipeline.core.orchestrator.questionnaire import (
	CanonicalQuestionnaire,
	load_questionnaire,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Processor Bundle (typed DI container)
# =============================================================================

@dataclass(frozen=True)
class ProcessorBundle:
	"""Aggregated orchestrator dependencies built by the Factory.

	Attributes:
		method_executor: Preconfigured MethodExecutor ready for routing.
		questionnaire: Immutable, validated CanonicalQuestionnaire.
		signal_registry: QuestionnaireSignalRegistry with full metadata.
		executor_config: Canonical ExecutorConfig for executors.
		enriched_signal_packs: Optional dict of EnrichedSignalPack per policy area.
	"""

	method_executor: MethodExecutor
	questionnaire: CanonicalQuestionnaire
	signal_registry: QuestionnaireSignalRegistry
	executor_config: ExecutorConfig
	enriched_signal_packs: Optional[dict[str, Any]] = None


# =============================================================================
# Core Factory API
# =============================================================================

def build_processor(
	*,
	executor_config: ExecutorConfig | None = None,
	enable_enriched_signals: bool = True,
) -> ProcessorBundle:
	"""Create a processor bundle with canonical DI wiring.

	Steps (strict order):
	1. Load canonical questionnaire (singleton + hash/structure validation).
	2. Build QuestionnaireSignalRegistry from the canonical data.
	3. Initialize MethodRegistry and configure special instantiation rules.
	4. Construct MethodExecutor with signal registry and method registry.
	5. Optionally build EnrichedSignalPack per policy area for executors.

	Returns:
		ProcessorBundle with all dependencies pre-wired.
	"""

	# 1) Canonical monolith access — single source of truth
	canonical: CanonicalQuestionnaire = load_questionnaire()
	logger.info(
		"canonical_questionnaire_loaded sha256=%s version=%s questions=%s",
		canonical.sha256[:16],
		canonical.version,
		canonical.total_question_count,
	)

	# 2) Signals — modern registry only (legacy loaders are deprecated)
	signal_registry: QuestionnaireSignalRegistry = _create_signal_registry(canonical)
	logger.info(
		"signal_registry_initialized policy_areas=%s",
		len(signal_registry.list_policy_areas()),
	)

	# 3) MethodRegistry with special instantiation rules
	method_registry = MethodRegistry()
	setup_default_instantiation_rules(method_registry)
	logger.info("method_registry_configured special_rules_applied")

	# 4) MethodExecutor wired to registry + signals
	method_executor = MethodExecutor(
		signal_registry=signal_registry,
		method_registry=method_registry,
	)

	# 5) Optional — build enriched packs (semantic expansion, context scoping)
	enriched_packs: Optional[dict[str, Any]] = None
	if enable_enriched_signals:
		enriched_packs = {}
		for pa_id in signal_registry.list_policy_areas():
			base_pack = signal_registry.get(pa_id)
			if base_pack is None:
				logger.warning("signal_pack_missing policy_area=%s", pa_id)
				continue
			enriched_packs[pa_id] = create_enriched_signal_pack(
				base_pack,
				enable_semantic_expansion=True,
			)
		logger.info(
			"enriched_signal_packs_built count=%s",
			len(enriched_packs),
		)

	effective_config = executor_config or ExecutorConfig()

	return ProcessorBundle(
		method_executor=method_executor,
		questionnaire=canonical,
		signal_registry=signal_registry,
		executor_config=effective_config,
		enriched_signal_packs=enriched_packs,
	)


def create_orchestrator(
	*,
	executor_config: ExecutorConfig | None = None,
	enable_enriched_signals: bool = True,
) -> Orchestrator:
	"""Create an Orchestrator instance with strict DI from Factory.

	Injection summary:
	- CanonicalQuestionnaire → Orchestrator(questionnaire=...)
	- MethodExecutor → Orchestrator(method_executor=...)
	- ExecutorConfig → Orchestrator(executor_config=...)
	- Signal registries are available via MethodExecutor; executors access packs
	  indirectly through routed methods (no direct file access).
	"""

	bundle = build_processor(
		executor_config=executor_config,
		enable_enriched_signals=enable_enriched_signals,
	)

	orchestrator = Orchestrator(
		method_executor=bundle.method_executor,
		questionnaire=bundle.questionnaire,
		executor_config=bundle.executor_config,
	)

	logger.info("orchestrator_created di_ok=true")
	return orchestrator


# =============================================================================
# Executor Wiring Helpers (Optional use by higher layers)
# =============================================================================

def get_enriched_pack_for_policy_area(
	bundle: ProcessorBundle, policy_area_id: str
) -> Any | None:
	"""Retrieve EnrichedSignalPack for a policy area, if available.

	Executors should receive this via their own factory/wiring functions
	(indirect injection) rather than reaching into the registry themselves.
	"""
	packs = bundle.enriched_signal_packs or {}
	return packs.get(policy_area_id)


__all__ = [
	"ProcessorBundle",
	"build_processor",
	"create_orchestrator",
	"get_enriched_pack_for_policy_area",
]

