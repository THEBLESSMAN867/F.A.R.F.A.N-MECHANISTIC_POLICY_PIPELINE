"""
Method Inventory Types Module.

Defines the immutable data structures for the static method inventory system.
This module is designed to be pure and dependency-free regarding the rest of the system.
"""
from dataclasses import dataclass
from typing import NewType

# MethodId: Unique identifier for a method (ClassName.method_name or function_name)
MethodId = NewType("MethodId", str)

@dataclass(frozen=True)
class ParameterDescriptor:
    """Describes a single parameter with full metadata."""
    name: str
    type_hint: str | None
    has_default: bool
    required: bool
    default_value: str | None
    default_type: str | None
    default_source: str | None

@dataclass(frozen=True)
class SignatureDescriptor:
    """Describes the signature of a method."""
    args: list[str]
    kwargs: list[str]
    returns: str
    accepts_executor_config: bool
    is_async: bool
    input_parameters: list[ParameterDescriptor] | None = None
    requiere_parametrizacion: bool = False

@dataclass(frozen=True)
class GovernanceFlags:
    """Flags related to governance and 'SIN_CARRETA' rules."""
    uses_yaml: bool
    has_hardcoded_calibration: bool
    has_hardcoded_timeout: bool
    suspicious_magic_numbers: list[str]
    is_executor_class: bool

@dataclass(frozen=True)
class LocationInfo:
    """Physical location of the method definition."""
    file_path: str
    line_start: int
    line_end: int

@dataclass(frozen=True)
class MethodDescriptor:
    """Complete descriptor for a single analytical method."""
    method_id: MethodId
    role: str  # EXTRACTOR|VALIDATOR|SCORER|AGGREGATOR|INGEST_PDM|META_TOOL
    aggregation_level: str  # INGEST|SCORE_Q|AGGREGATE|META
    module: str
    class_name: str | None
    method_name: str
    signature: SignatureDescriptor
    governance_flags: GovernanceFlags
    location: LocationInfo

@dataclass(frozen=True)
class MethodInventory:
    """The complete inventory of methods."""
    methods: dict[MethodId, MethodDescriptor]
    _version: str = "1.0.0"
    _comment: str = "Static unified method inventory for SAAAAAA – auto-generated, DO NOT EDIT BY HAND."
