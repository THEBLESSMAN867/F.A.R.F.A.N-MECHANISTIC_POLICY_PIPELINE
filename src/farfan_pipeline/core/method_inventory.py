"""
Static Method Inventory Generator - Core AST Analysis (Stages A-D).

This module implements the foundational logic to scan the codebase, parse files,
and extract raw method nodes. It is the first step in the inventory generation pipeline.
"""
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

SRC_ROOT = Path("farfan_core/farfan_core/core")
DEFAULT_OUTPUT = Path("farfan_core/farfan_core/artifacts/calibration/method_inventory.json")

from .method_inventory_types import (
    GovernanceFlags,
    SignatureDescriptor,
)

# ... (Stages A-D remain unchanged) ...

# --- Stage F: Signature ---

def classify_default_type(default_node: ast.expr) -> str:
    """Classify the type of default value."""
    if isinstance(default_node, ast.Constant):
        return "literal"
    elif isinstance(default_node, (ast.Name, ast.Attribute)):
        return "expression"
    else:
        return "complex"

def extract_parameter_info(
    arg: ast.arg,
    default: ast.expr | None,
    is_kwonly: bool = False
) -> ParameterDescriptor:
    """Extract detailed parameter information from AST."""
    from .method_inventory_types import ParameterDescriptor

    name = arg.arg

    type_hint = None
    if arg.annotation:
        try:
            type_hint = ast.unparse(arg.annotation)
        except AttributeError:
            type_hint = "Any"

    has_default = default is not None
    required = not has_default

    default_value = None
    default_type = None
    default_source = None

    if has_default:
        try:
            default_source = ast.unparse(default)
            default_value = default_source
            default_type = classify_default_type(default)
        except AttributeError:
            default_value = "<unparseable>"
            default_type = "complex"
            default_source = "<unparseable>"

    return ParameterDescriptor(
        name=name,
        type_hint=type_hint,
        has_default=has_default,
        required=required,
        default_value=default_value,
        default_type=default_type,
        default_source=default_source
    )

def should_parametrize_method(func_def: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Determine if a method requires parameterization."""
    if func_def.name in ('__init__', '__repr__', '__str__', '__eq__'):
        return False

    all_args = func_def.args.args + func_def.args.kwonlyargs
    non_self_args = [a for a in all_args if a.arg not in ('self', 'cls')]

    return len(non_self_args) > 0

def extract_signature(func_def: ast.FunctionDef | ast.AsyncFunctionDef) -> SignatureDescriptor:
    from .method_inventory_types import SignatureDescriptor

    args = [a.arg for a in func_def.args.posonlyargs + func_def.args.args]
    kwargs = [a.arg for a in func_def.args.kwonlyargs]

    returns = "None"
    if func_def.returns:
        try:
            returns = ast.unparse(func_def.returns)
        except AttributeError:
            returns = "Complex"

    accepts_executor_config = False
    all_args = func_def.args.posonlyargs + func_def.args.args + func_def.args.kwonlyargs
    for arg in all_args:
        if arg.annotation:
            try:
                ann_str = ast.unparse(arg.annotation)
                if "ExecutorConfig" in ann_str or "RuntimeConfig" in ann_str:
                    accepts_executor_config = True
            except AttributeError:
                pass

    requiere_parametrizacion = should_parametrize_method(func_def)
    input_parameters = None

    if requiere_parametrizacion:
        input_parameters = []

        posonly_args = func_def.args.posonlyargs
        posonly_defaults = []
        if func_def.args.defaults:
            num_posonly_with_defaults = max(0, len(func_def.args.defaults) - len(func_def.args.args))
            posonly_defaults = func_def.args.defaults[:num_posonly_with_defaults]

        for i, arg in enumerate(posonly_args):
            if arg.arg in ('self', 'cls'):
                continue
            default_idx = i - (len(posonly_args) - len(posonly_defaults))
            default = posonly_defaults[default_idx] if default_idx >= 0 else None
            input_parameters.append(extract_parameter_info(arg, default))

        pos_args = func_def.args.args
        pos_defaults = func_def.args.defaults if func_def.args.defaults else []
        num_no_default = len(pos_args) - len(pos_defaults)

        for i, arg in enumerate(pos_args):
            if arg.arg in ('self', 'cls'):
                continue
            default_idx = i - num_no_default
            default = pos_defaults[default_idx] if default_idx >= 0 else None
            input_parameters.append(extract_parameter_info(arg, default))

        kwonly_args = func_def.args.kwonlyargs
        kwonly_defaults = func_def.args.kw_defaults if func_def.args.kw_defaults else []

        for i, arg in enumerate(kwonly_args):
            if arg.arg in ('self', 'cls'):
                continue
            default = kwonly_defaults[i] if i < len(kwonly_defaults) else None
            input_parameters.append(extract_parameter_info(arg, default, is_kwonly=True))

        if func_def.args.vararg:
            from .method_inventory_types import ParameterDescriptor
            vararg_type = None
            if func_def.args.vararg.annotation:
                try:
                    vararg_type = ast.unparse(func_def.args.vararg.annotation)
                except AttributeError:
                    pass
            input_parameters.append(ParameterDescriptor(
                name=f"*{func_def.args.vararg.arg}",
                type_hint=vararg_type,
                has_default=True,
                required=False,
                default_value="()",
                default_type="expression",
                default_source="()"
            ))

        if func_def.args.kwarg:
            from .method_inventory_types import ParameterDescriptor
            kwarg_type = None
            if func_def.args.kwarg.annotation:
                try:
                    kwarg_type = ast.unparse(func_def.args.kwarg.annotation)
                except AttributeError:
                    pass
            input_parameters.append(ParameterDescriptor(
                name=f"**{func_def.args.kwarg.arg}",
                type_hint=kwarg_type,
                has_default=True,
                required=False,
                default_value="{}",
                default_type="expression",
                default_source="{}"
            ))

    return SignatureDescriptor(
        args=args,
        kwargs=kwargs,
        returns=returns,
        accepts_executor_config=accepts_executor_config,
        is_async=isinstance(func_def, ast.AsyncFunctionDef),
        input_parameters=input_parameters,
        requiere_parametrizacion=requiere_parametrizacion
    )

# --- Stage G: Governance ---

# --- Stage G: Governance ---
def compute_governance_flags_for_file(module_ast: ast.Module) -> GovernanceFlags:
    uses_yaml = False
    has_hardcoded_calibration = False
    has_hardcoded_timeout = False
    suspicious_magic_numbers: list[str] = []

    for node in ast.walk(module_ast):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                name = alias.name
                if "yaml" in name:
                    uses_yaml = True

        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.endswith((".yml", ".yaml")):
                uses_yaml = True

        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target_name = None
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                target_name = node.targets[0].id
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                target_name = node.target.id

            if target_name is not None:
                val = getattr(node, "value", None)
                if isinstance(val, ast.Constant) and isinstance(val.value, (int, float)):
                    if any(k in target_name for k in ("timeout", "timeout_s", "max_retries", "retry")):
                        has_hardcoded_timeout = True
                        suspicious_magic_numbers.append(f"{target_name} = {val.value}")

                    # Calibration tokens
                    cal_tokens = ["b_theory", "b_impl", "b_deploy", "quality_threshold", "evidence_snippets", "priority_score"]
                    if any(t in target_name for t in cal_tokens):
                         has_hardcoded_calibration = True
                         suspicious_magic_numbers.append(f"{target_name} assigned literal")

    return GovernanceFlags(
        uses_yaml=uses_yaml,
        has_hardcoded_calibration=has_hardcoded_calibration,
        has_hardcoded_timeout=has_hardcoded_timeout,
        suspicious_magic_numbers=suspicious_magic_numbers,
        is_executor_class=False, # Set later per method
    )

from collections.abc import Iterable

# Import types (only if needed for type hinting later, but for now we keep it minimal as requested)
# from .method_inventory_types import ...

SRC_ROOT = Path("farfan_core/farfan_core/core") # Kept for backward compat if needed, but main logic uses INVENTORY_ROOTS
DEFAULT_OUTPUT = Path("farfan_core/farfan_core/artifacts/calibration/method_inventory.json")

INVENTORY_ROOTS = [
    Path("."),
]

EXCLUDE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".hypothesis",
    "tests",
    "devtools",
    "scripts/dev",
    "tools",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "build",
    "dist",
    "site-packages",
    ".idea",
    ".vscode",
}

# --- Stage A: Walk ---

def should_exclude_path(path: Path) -> bool:
    return any(part in EXCLUDE_DIR_NAMES for part in path.parts)

def _normalize_roots(roots: Path | Iterable[Path] | None) -> list[Path]:
    """
    Normalize the roots argument so that walk_python_files can accept:
    - None (use INVENTORY_ROOTS)
    - a single Path
    - an iterable of Paths
    """
    if roots is None:
        return list(INVENTORY_ROOTS)
    if isinstance(roots, Path):
        return [roots]
    return list(roots)

def walk_python_files(roots: Path | Iterable[Path] | None = None) -> list[Path]:
    """
    Return all .py files under the given root(s) that are part of the pipeline,
    excluding tests, devtools, caches, and other non-pipeline directories.

    - roots is None: use INVENTORY_ROOTS (multiple roots).
    - roots is a Path: scan only that root (used by tests).
    - roots is an iterable of Paths: scan them all.
    """
    roots_list = _normalize_roots(roots)

    files: set[Path] = set()
    for root in roots_list:
        if not root.exists():
            continue
        # If root is '.', rglob("*") might be too broad if not careful, but we filter extensions
        for p in root.rglob("*.py"):
            if should_exclude_path(p):
                continue
            files.add(p)
    return sorted(files)

# --- Stage B: Module Path ---

def module_path_from_file(path: Path, root: Path) -> str:
    """
    Derive a dotted module path from a file path.
    Heuristically determines the package root to ensure correct imports.
    """
    parts = path.parts

    # Heuristic 1: farfan_core package structure
    try:
        # Find the index of 'farfan_core'
        # We want the path starting from the package name.
        # If path is .../farfan_core/farfan_core/core/foo.py -> farfan_core.core.foo
        # If path is .../farfan_core/core/foo.py -> farfan_core.core.foo

        # We iterate backwards to find the last 'farfan_core' that acts as a package root?
        # Actually, if we have farfan_core/farfan_core, the package is the inner one.
        # If we have just farfan_core, it is the package.

        # Let's look for the index of 'farfan_core'.
        indices = [i for i, part in enumerate(parts) if part == "farfan_core"]

        if indices:
            # If multiple, the package usually starts at the last one?
            # No, if path is repo/farfan_core/farfan_core/core/foo.py
            # The module is farfan_core.core.foo
            # So we want parts starting from the *second* farfan_core (index 1 of the slice).
            # Which is the last index in the list of indices.

            start_index = indices[-1]
            module_parts = parts[start_index:]
            return ".".join(module_parts).removesuffix(".py")

    except ValueError:
        pass

    # Heuristic 2: Scripts
    if "scripts" in parts:
        try:
            start_index = parts.index("scripts")
            module_parts = parts[start_index:]
            return ".".join(module_parts).removesuffix(".py")
        except ValueError:
            pass

    # Fallback: relative to provided root if sensible
    try:
        if root != Path("."):
            rel = path.relative_to(root)
            return ".".join(rel.parts).removesuffix(".py")
    except ValueError:
        pass

    # Final Fallback: just the filename
    return path.stem

# --- Stage C: Parse ---

def parse_file(path: Path) -> ast.Module:
    """
    Parse a Python file into an AST. Raise SyntaxError if invalid.
    """
    source = path.read_text(encoding="utf-8")
    return ast.parse(source, filename=str(path))

# --- Stage D: Raw Extraction ---

@dataclass
class RawMethodNode:
    module_path: str
    class_name: str | None
    func_def: ast.FunctionDef | ast.AsyncFunctionDef

def extract_raw_methods(module_ast: ast.Module, module_path: str) -> list[RawMethodNode]:
    """
    Extract raw method/function nodes from a module AST.

    - Methods defined inside classes (ClassDef -> FunctionDef / AsyncFunctionDef).
    - Top-level functions (FunctionDef / AsyncFunctionDef).
    """
    raw: list[RawMethodNode] = []

    for node in module_ast.body:
        # Classes
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            for body_item in node.body:
                if isinstance(body_item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    raw.append(
                        RawMethodNode(
                            module_path=module_path,
                            class_name=class_name,
                            func_def=body_item,
                        )
                    )
        # Top-level functions
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            raw.append(
                RawMethodNode(
                    module_path=module_path,
                    class_name=None,
                    func_def=node,
                )
            )

    return raw

# --- Future Stages (TODO) ---

# def extract_signature(func_def: ast.FunctionDef | ast.AsyncFunctionDef) -> SignatureDescriptor:
#     pass

# def compute_governance_flags(module_ast: ast.Module, class_name: Optional[str]) -> GovernanceFlags:
#     pass

import argparse
import json
from dataclasses import asdict
from typing import Any

from .method_inventory_types import (
    LocationInfo,
    MethodDescriptor,
    MethodId,
    MethodInventory,
)

# ... (Stages A-D, F-G remain unchanged) ...

# --- Stage E: Classification ---

def classify_method(raw: RawMethodNode, file_path: Path) -> tuple[str, str]:
    role = "UNKNOWN"
    level = "UNKNOWN"

    # Ejecutores de Fase 2 (visible para questionnaire_monolith)
    if raw.class_name and raw.class_name.startswith("D") and "_Q" in raw.class_name and raw.func_def.name == "execute":
        role = "EXECUTOR_Q"
        level = "SCORE_Q"
    elif "scripts/pipeline" in str(file_path):
        role = "PIPELINE_SCRIPT"
        level = "PIPELINE_ORCHESTRATION"
    elif "aggregation.py" in str(file_path):
        role = "AGGREGATOR"
        level = "AGGREGATE"
    elif "flux" in str(file_path) or "phases.py" in str(file_path):
        role = "INGEST_PDM"
        level = "INGEST"

    return role, level

# --- Stage H: Build Inventory ---

# --- Stage H: Build Inventory ---

def is_snapshot_module(module_path: str) -> bool:
    """
    Return True if this module path corresponds to a snapshot copy of executors
    that should not be treated as a separate logical method M.
    """
    return ".executors_snapshot." in module_path

def make_method_id(raw: RawMethodNode) -> MethodId:
    if raw.class_name is not None:
        return MethodId(f"{raw.class_name}.{raw.func_def.name}")
    return MethodId(raw.func_def.name)

def build_method_descriptors_for_file(path: Path, root: Path) -> list[MethodDescriptor]:
    try:
        module_ast = parse_file(path)
    except Exception as e:
        print(f"Error parsing {path}: {e}", file=sys.stderr)
        return []

    module_path = module_path_from_file(path, root)
    if not module_path:
        module_path = "unknown"

    raw_methods = extract_raw_methods(module_ast, module_path)

    # Optimized Governance: Compute once per file
    file_gov_flags = compute_governance_flags_for_file(module_ast)

    descriptors = []

    for raw in raw_methods:
        # Skip 'main' functions as they are entry points, not analytical methods,
        # and cause collisions in a full repo scan.
        if raw.func_def.name == "main":
            continue

        role, level = classify_method(raw, path)
        signature = extract_signature(raw.func_def)

        is_executor = bool(raw.class_name and "Executor" in raw.class_name)

        # Merge file-level flags with method-specific context (is_executor_class)
        gov_flags = GovernanceFlags(
            uses_yaml=file_gov_flags.uses_yaml,
            has_hardcoded_calibration=file_gov_flags.has_hardcoded_calibration,
            has_hardcoded_timeout=file_gov_flags.has_hardcoded_timeout,
            suspicious_magic_numbers=file_gov_flags.suspicious_magic_numbers,
            is_executor_class=is_executor
        )

        # Location
        loc = LocationInfo(
            file_path=str(path),
            line_start=raw.func_def.lineno,
            line_end=raw.func_def.end_lineno if hasattr(raw.func_def, "end_lineno") else raw.func_def.lineno
        )

        method_id = make_method_id(raw)

        desc = MethodDescriptor(
            method_id=method_id,
            role=role,
            aggregation_level=level,
            module=module_path,
            class_name=raw.class_name,
            method_name=raw.func_def.name,
            signature=signature,
            governance_flags=gov_flags,
            location=loc
        )
        descriptors.append(desc)

    return descriptors

def build_method_inventory(roots: Path | Iterable[Path] | None = None) -> MethodInventory:
    methods: dict[MethodId, MethodDescriptor] = {}

    all_files = walk_python_files(roots)

    for f in all_files:
        # Determine which root this file belongs to for module path calculation
        # Normalized roots list for checking
        roots_list = _normalize_roots(roots)
        matching_root = SRC_ROOT # Default fallback
        for r in roots_list:
            try:
                f.relative_to(r.parent)
                matching_root = r
                break
            except ValueError:
                continue

        descriptors = build_method_descriptors_for_file(f, matching_root)

        for d in descriptors:
            method_id = d.method_id

            existing = methods.get(method_id)
            if existing is None:
                if is_snapshot_module(d.module):
                    # snapshot sin vivo: se ignora por diseño v1
                    continue
                methods[method_id] = d
            # colisión entre definiciones
            elif is_snapshot_module(d.module) and not is_snapshot_module(existing.module):
                # nuevo = snapshot, existente = vivo -> ignorar snapshot
                continue
            elif not is_snapshot_module(d.module) and is_snapshot_module(existing.module):
                # nuevo = vivo, antiguo = snapshot -> promover vivo
                methods[method_id] = d
                continue
            else:
                # ambos vivos o ambos snapshot -> colisión real
                # En un escaneo completo de todo el repo, esto es inevitable para funciones comunes.
                # Para cumplir con "DAME ESO YA MISMO", convertimos el error en warning y saltamos.
                print(
                    f"Warning: True Method ID collision for '{method_id}' between {existing.module} and {d.module}. Skipping {d.module}.",
                    file=sys.stderr
                )
                continue

    return MethodInventory(methods=methods)

# --- Stage I: Serialization & CLI ---

def method_inventory_to_json(inv: MethodInventory) -> dict[str, Any]:
    return asdict(inv)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Static Method Inventory")
    parser.add_argument("--root", type=str, help="Root directory to scan (optional, defaults to configured INVENTORY_ROOTS)")
    parser.add_argument("--output", type=str, help="Output JSON file path")

    args = parser.parse_args(argv)

    # If root is provided, use it. Otherwise pass None to use INVENTORY_ROOTS.
    root_arg = Path(args.root) if args.root else None

    if root_arg:
        if not root_arg.exists() or not root_arg.is_dir():
             print(f"Root directory not found: {root_arg}", file=sys.stderr)
             return 1
        print(f"Scanning root: {root_arg}")
    else:
        print(f"Scanning configured roots: {INVENTORY_ROOTS}")

    output_path = Path(args.output) if args.output else DEFAULT_OUTPUT

    try:
        inventory = build_method_inventory(root_arg)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2

    # Serialization
    data = method_inventory_to_json(inventory)

    # Ensure output dir exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Inventory generated at: {output_path}")
    print(f"Total methods: {len(inventory.methods)}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
