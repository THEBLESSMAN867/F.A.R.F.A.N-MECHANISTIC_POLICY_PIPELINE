"""ParameterLoaderV2: Centralized parameter loading from canonical catalogue."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ParameterLoaderV2:
    """
    Centralized parameter loader that reads from canonical_method_catalogue_v2.json.
    Replaces scattered parameter_loader calls with single source of truth.
    """

    _instance: "ParameterLoaderV2 | None" = None
    _catalogue: dict[str, dict[str, Any]] | None = None
    _catalogue_path: Path | None = None

    def __new__(cls) -> "ParameterLoaderV2":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._catalogue is None:
            self._load_catalogue()

    def _load_catalogue(self) -> None:
        """Load canonical method catalogue from JSON file."""
        if self._catalogue_path is None:
            self._catalogue_path = (
                Path(__file__).parent / "canonical_method_catalogue_v2.json"
            )

        try:
            with open(self._catalogue_path, encoding="utf-8") as f:
                data = json.load(f)
                self._catalogue = data.get("methods", {})
                logger.info(
                    f"Loaded {len(self._catalogue)} methods from canonical catalogue v{data['metadata']['version']}"
                )
        except FileNotFoundError:
            logger.error(f"Canonical catalogue not found at {self._catalogue_path}")
            self._catalogue = {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse canonical catalogue: {e}")
            self._catalogue = {}

    @classmethod
    def get(cls, method_id: str, param_name: str, default: Any = None) -> Any:
        """
        Get a specific parameter value for a method.

        Args:
            method_id: Fully qualified method identifier
            param_name: Parameter name to retrieve
            default: Default value if parameter not found

        Returns:
            Parameter value or default
        """
        instance = cls()
        if instance._catalogue is None:
            return default

        method_params = instance._catalogue.get(method_id, {})
        return method_params.get(param_name, default)

    @classmethod
    def get_all(cls, method_id: str) -> dict[str, Any]:
        """
        Get all parameters for a method.

        Args:
            method_id: Fully qualified method identifier

        Returns:
            Dictionary of all parameters for the method
        """
        instance = cls()
        if instance._catalogue is None:
            return {}

        return instance._catalogue.get(method_id, {})

    @classmethod
    def reload(cls) -> None:
        """Force reload of the catalogue from disk."""
        if cls._instance is not None:
            cls._instance._load_catalogue()
