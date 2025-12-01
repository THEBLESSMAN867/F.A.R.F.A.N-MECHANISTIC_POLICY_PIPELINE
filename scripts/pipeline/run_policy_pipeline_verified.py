#!/usr/bin/env python3
"""
Compatibility wrapper that delegates to ``farfan_pipeline.scripts.run_policy_pipeline_verified``.

The real implementation now lives inside the package so the entrypoint
can be invoked via ``python -m farfan_pipeline.scripts.run_policy_pipeline_verified``.
"""

from __future__ import annotations

from farfan_pipeline.scripts.run_policy_pipeline_verified import cli


if __name__ == "__main__":
    cli()
