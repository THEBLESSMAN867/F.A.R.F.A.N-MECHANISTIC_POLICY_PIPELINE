"""Calibration decorators using centralized ParameterLoaderV2."""

import functools
import logging
from collections.abc import Callable
from typing import Any

from farfan_pipeline.core.parameters import ParameterLoaderV2

logger = logging.getLogger(__name__)


def calibrated_method(method_id: str) -> Callable:
    """
    Decorator to apply calibration to a method using centralized ParameterLoaderV2.

    Future: Will invoke CalibrationOrchestrator.calibrate(method_id, context) when available.

    Args:
        method_id: Fully qualified method identifier for parameter lookup

    Returns:
        Decorated function with calibration applied
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            calibration_params = ParameterLoaderV2.get_all(method_id)

            logger.debug(
                f"Calling calibrated method '{method_id}' with {len(calibration_params)} parameters"
            )

            # Future: CalibrationOrchestrator.calibrate(method_id, context={
            #     "args": args,
            #     "kwargs": kwargs,
            #     "params": calibration_params
            # })

            return func(*args, **kwargs)

        return wrapper

    return decorator
