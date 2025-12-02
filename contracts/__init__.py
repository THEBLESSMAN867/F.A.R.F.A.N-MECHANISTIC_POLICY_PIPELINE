"""
Legacy compatibility shim for the deprecated top-level `contracts` package.

Historically, downstream tooling imported `contracts` from the repository root.
The canonical contract definitions now live in `farfan_core.core.contracts`.
This shim keeps those imports functional and ensures that architectural tooling
placed under the `contracts/` directory (such as importlinter configs) does not
shadow or break runtime behavior.

DEPRECATED: This module is deprecated. Import from farfan_core.core.contracts instead.
"""

import warnings

from farfan_core.core.contracts import *  # noqa: F401,F403

warnings.warn(
    "Importing from top-level 'contracts' package is deprecated. "
    "Use 'from farfan_core.core.contracts import ...' instead. "
    "This shim will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)
