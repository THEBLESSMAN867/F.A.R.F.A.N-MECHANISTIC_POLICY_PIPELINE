# Contracts Folder Structure

This directory hosts all executable contracts (schemas, validators, enforcement configs). It follows the canonical labeling scheme:

```
contracts/
  current/        # Active production contracts (mandatory naming: CTR-{Phase|Subsystem}_{Name}_vX.Y.{ext})
  deprecated/     # Retired contracts kept only for traceability (same naming + `_DEPRECATED`)
  experimental/   # Non-production contract drafts (prefixed `EXP-`)
  tooling/        # Enforcement configs (e.g., import-linter) that support contract validation
```

- **Naming rule:** From the filename alone it must be obvious whether the artifact is current (`CTR-`), deprecated (`CTR-..._DEPRECATED`), or experimental (`EXP-`). Include phase identifiers when applicable (e.g., `CTR-P04_DimensionScoreSchema_v1.0.json`).
- **Migration plan:** Existing contract files (schemas under `schemas/`, validators in `src/saaaaaa/utils/validation/…`, etc.) will be relocated into `contracts/current/` with the new labels. Until each file is moved, its owning module must reference this plan and track the migration status.
- **Tooling:** Contract enforcement configurations live under `contracts/tooling/`. The root `__init__.py` exposes helper registries for runtime validation.
- **Archive policy:** Moving a contract to `contracts/deprecated/` requires updating the referencing phase document and code to point at the new replacement.
