"""Farfan Core Package Initialization.

DEPRECATED: get_parameter_loader() is deprecated.
Use ParameterLoaderV2 directly: from farfan_pipeline.core.parameters import ParameterLoaderV2
"""

from .core.calibration.parameter_loader import ParameterLoader
from .core.parameters import ParameterLoaderV2

_parameter_loader = None


def get_parameter_loader() -> "ParameterLoader":
    """
    DEPRECATED: Use ParameterLoaderV2.get(method_id, param_name) instead.
    
    This function is kept for backward compatibility only.
    Singleton global - guarantees EVERYONE uses the same one.
    """
    global _parameter_loader

    if _parameter_loader is None:
        _parameter_loader = ParameterLoader()
        _parameter_loader.load()

    return _parameter_loader


__all__ = ["get_parameter_loader", "ParameterLoaderV2"]
