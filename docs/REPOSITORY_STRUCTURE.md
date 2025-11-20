# Repository Structure (Canonical Map)

This document codifies the deterministic directory graph `R`. Every top-level folder must map to a phase, subsystem, or tooling module. Any folder not listed here is treated as non-canonical and must be either removed or explicitly registered.

| Path | Purpose | Governing Doc / Phase |
| --- | --- | --- |
| `config/` | Canonical runtime and questionnaire configuration assets. | Phase 0 (`docs/phases/phase_0/…`) |
| `contracts/` | Active enforcement artifacts (schemas, validators). A forthcoming contract-labeling plan will reorganize its internals per the new standard. | All phases (cross-cutting) |
| `data/` | Canonical questionnaire resources, calibration datasets, static inputs referenced by the pipeline. | Phase 0 / ingestion |
| `docs/` | Documentation tree. Phase doctrines live under `docs/phases/`; historical material is quarantined under `docs/archive/`. | System-wide |
| `examples/` | Demonstrative notebooks/scripts for integration tests. | Tooling |
| `metricas_y_seguimiento_canonico/` | Canonical metrics subsystem (`health.py`, `metrics.py`). Must retain README.md describing allowed APIs. | Cross-cutting telemetry |
| `minipdm/` | Mini PDM harness (artifacts/config/controls). Active subsystem until reclassified; see `minipdm/README.md`. | Experimental ingestion |
| `reports/` | Generated or curated audit reports (JSON/MD). Each report references the phase it covers. | Auditing |
| `rules/` | Rule definitions consumed by orchestrator/executors. | Phases 3–7 |
| `schemas/` | JSON/schema definitions, pending migration into contract hierarchy. | Contracts |
| `scripts/` | Verified tooling scripts for audits, installers, and diagnostics. | Tooling |
| `spc_ingestion/` | SPC ingestion engine (Phase 1). | Phase 1 |
| `src/` | Main application source (orchestrator, processing, analysis). | All phases |
| `tests/` | Authoritative test suites. | QA |
| `tools/` | CLI helpers, analyzers, and secondary automation. | Tooling |

**Removed/Archived Paths**
- `logs/`, `output/`, `tmp/`, `causal_exctractor_2`, `fix_2`, and the `FASE_*` docs have been relocated to `docs/archive/` or deleted to keep the canonical tree clean.

**Obligations**
- Any new folder must be added to this table with a clear purpose and documentation reference.
- Ambiguous legacy folders must either be renamed to follow the pattern above or moved under `docs/archive/` / `legacy/`.
- Contracts folder to be reorganized under the forthcoming labeling scheme (current vs deprecated vs experimental).
