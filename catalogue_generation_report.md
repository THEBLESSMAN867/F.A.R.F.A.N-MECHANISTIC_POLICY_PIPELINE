================================================================
CATÁLOGO V2 - REPORTE DE GENERACIÓN
================================================================

ESTADÍSTICAS:
  Total methods scanned: 2181
  Methods successfully parsed: 2181 (100%)
  Methods with parsing errors: 0

  Methods with configurable params: 429 (19.7%)
  Total parameters: 3383
  Configurable parameters: 786 (23.2%)

DISTRIBUCIÓN DE DEFAULTS:
  Literal values: 750 (95.4%)
  Evaluated expressions: 0 (0.0%)
  Complex expressions: 36 (4.6%)

VERIFICACIONES:
  ✅ Test 1 (Consistency): PENDING
  ✅ Test 2 (Source Match): PENDING
  ✅ Test 3 (Coverage): PENDING
  ✅ Test 4 (Known Methods): PENDING

ARCHIVO GENERADO:
  Path: canonical_method_catalogue_v2.json
  Size: 3.5 MB
  Methods: 2181
  Valid JSON: ✅

CAMBIOS vs CATÁLOGO VIEJO:
  Methods added: 443
  Methods removed: 257
  Parameters updated: 786
  Fields added per method: 4 (has_default, default_value, default_type, default_source)

TOP 10 METHODS WITH MOST CONFIGURABLES:
  1. src.saaaaaa.flux.cli.run: 22 configurable params
  2. src.saaaaaa.core.orchestrator.core.Orchestrator.__init__: 11 configurable params
  3. src.saaaaaa.core.orchestrator.executor_config.ExecutorConfig.from_cli_args: 10 configurable params
  4. src.saaaaaa.processing.policy_processor.IndustrialPolicyProcessor.__init__: 9 configurable params
  5. src.saaaaaa.core.orchestrator.evidence_registry.EvidenceRecord.create: 7 configurable params
  6. src.saaaaaa.core.orchestrator.signals.SignalClient.__init__: 7 configurable params
  7. src.saaaaaa.core.calibration.orchestrator.CalibrationOrchestrator.__init__: 6 configurable params
  8. src.saaaaaa.core.orchestrator.core.ResourceLimits.__init__: 6 configurable params
  9. src.saaaaaa.core.orchestrator.evidence_registry.EvidenceRegistry.record_evidence: 6 configurable params
  10. src.saaaaaa.patterns.event_tracking.EventTracker.filter_events: 6 configurable params

MÉTODOS CON DEFAULTS COMPLEJOS (revisar):
  - src.saaaaaa.analysis.bayesian_multilevel_system.MultiLevelBayesianOrchestrator.__init__: param="output_dir" default="Path('data/bayesian_outputs')"
  - src.saaaaaa.analysis.contradiction_deteccion.PolicyContradictionDetector.__init__: param="device" default="'cuda' if torch.cuda.is_available() else 'cpu'"
  - src.saaaaaa.analysis.contradiction_deteccion.PolicyContradictionDetector.detect: param="dimension" default="PolicyDimension.ESTRATEGICO"
  - src.saaaaaa.analysis.teoria_cambio.AdvancedDAGValidator.__init__: param="graph_type" default="GraphType.CAUSAL_DAG"
  - src.saaaaaa.api.api_server.cached: param="ttl" default="APIConfig.CACHE_TTL"
  - src.saaaaaa.flux.cli.run: param="aggregate_feature_set" default="typer.Option('full', help='Feature set (minimal/full)')"
  - src.saaaaaa.flux.cli.run: param="aggregate_group_by" default="typer.Option('policy_area,year', help='Aggregation keys (comma-separated)')"
  - src.saaaaaa.flux.cli.run: param="chunk_max_tokens_meso" default="typer.Option(1200, help='Max tokens for meso')"
  - src.saaaaaa.flux.cli.run: param="chunk_max_tokens_micro" default="typer.Option(400, help='Max tokens for micro')"
  - src.saaaaaa.flux.cli.run: param="chunk_overlap_max" default="typer.Option(0.15, help='Max overlap fraction')"
  - src.saaaaaa.flux.cli.run: param="chunk_priority_resolution" default="typer.Option('MESO', help='Priority resolution (MICRO/MESO/MACRO)')"
  - src.saaaaaa.flux.cli.run: param="dry_run" default="typer.Option(False, help='Dry run (validation only)')"
  - src.saaaaaa.flux.cli.run: param="ingest_enable_ocr" default="typer.Option(True, help='Enable OCR')"
  - src.saaaaaa.flux.cli.run: param="ingest_max_mb" default="typer.Option(250, help='Max file size in MB')"
  - src.saaaaaa.flux.cli.run: param="ingest_ocr_threshold" default="typer.Option(0.85, help='OCR threshold')"
  - src.saaaaaa.flux.cli.run: param="input_uri" default="typer.Argument(..., help='Input document URI')"
  - src.saaaaaa.flux.cli.run: param="normalize_keep_diacritics" default="typer.Option(True, help='Keep diacritics')"
  - src.saaaaaa.flux.cli.run: param="normalize_unicode_form" default="typer.Option('NFC', help='Unicode form (NFC/NFKC)')"
  - src.saaaaaa.flux.cli.run: param="print_contracts" default="typer.Option(False, help='Print contracts and exit')"
  - src.saaaaaa.flux.cli.run: param="report_formats" default="typer.Option('json,md', help='Report formats (comma-separated)')"

================================================================
RESULTADO: ⚠️ PENDING VALIDATION
================================================================