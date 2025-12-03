#!/usr/bin/env python3
"""
Generate Canonical Method Inventory with Three Outputs:
1. canonical_method_inventory.json - Full inventory with signatures
2. method_statistics.json - Statistics by role, module, executors
3. excluded_methods.json - Methods flagged as 'never calibrate'
"""

import ast
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

TRIVIAL_FORMATTERS = {
    "__str__",
    "__repr__",
    "__init__",
    "__del__",
    "__format__",
    "to_string",
    "to_json",
    "to_dict",
    "from_dict",
    "__eq__",
    "__ne__",
    "__hash__",
    "__lt__",
    "__le__",
    "__gt__",
    "__ge__",
}

ROLE_PATTERNS = {
    "executor": ["execute", "run_executor", "perform", "apply"],
    "orchestrator": ["orchestrate", "coordinate", "run", "execute_suite", "build"],
    "analyzer": ["analyze", "infer", "calculate", "compute", "assess"],
    "processor": ["process", "transform", "clean", "normalize", "aggregate"],
    "extractor": ["extract", "identify", "detect", "find", "locate"],
    "scorer": ["score", "evaluate", "rate", "rank", "measure"],
    "ingestor": ["parse", "load", "read", "extract_raw", "ingest"],
    "utility": ["_format", "_helper", "_validate", "_check", "_get", "_set"],
    "core": ["__init__", "setup", "initialize", "configure"],
}


class CanonicalMethodScanner(ast.NodeVisitor):
    def __init__(self, module_path: str, file_path: str):
        self.module_path = module_path
        self.file_path = file_path
        self.methods = []
        self.current_class = None
        self.class_stack = []
        self.function_depth = 0

    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.current_class = ".".join(self.class_stack)
        self.generic_visit(node)
        self.class_stack.pop()
        self.current_class = ".".join(self.class_stack) if self.class_stack else None

    def visit_FunctionDef(self, node):
        if self.function_depth == 0:
            self._register_method(node)
        self.function_depth += 1
        self.generic_visit(node)
        self.function_depth -= 1

    def visit_AsyncFunctionDef(self, node):
        if self.function_depth == 0:
            self._register_method(node)
        self.function_depth += 1
        self.generic_visit(node)
        self.function_depth -= 1

    def _register_method(self, node):
        method_name = node.name
        if self.current_class:
            canonical_name = f"{self.module_path}.{self.current_class}.{method_name}"
        else:
            canonical_name = f"{self.module_path}.{method_name}"
        self.methods.append((canonical_name, node.lineno, self.current_class, node))


def extract_signature(node):
    parameters = []
    args = node.args

    def get_type_hint(arg):
        if arg.annotation:
            try:
                return ast.unparse(arg.annotation)
            except:
                return None
        return None

    def get_default_repr(default):
        try:
            return ast.unparse(default)
        except:
            return "..."

    all_args = args.args + args.posonlyargs + args.kwonlyargs
    defaults = [None] * (len(all_args) - len(args.defaults)) + list(args.defaults)

    param_kinds = []
    for arg in args.posonlyargs:
        param_kinds.append((arg, "POSITIONAL_ONLY"))
    for arg in args.args:
        param_kinds.append((arg, "POSITIONAL_OR_KEYWORD"))
    if args.vararg:
        param_kinds.append((args.vararg, "VAR_POSITIONAL"))
    for arg in args.kwonlyargs:
        param_kinds.append((arg, "KEYWORD_ONLY"))
    if args.kwarg:
        param_kinds.append((args.kwarg, "VAR_KEYWORD"))

    kw_defaults = args.kw_defaults if args.kw_defaults else []

    for idx, (arg, kind) in enumerate(param_kinds):
        if kind in ("POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"):
            default_val = defaults[idx] if idx < len(defaults) else None
        elif kind == "KEYWORD_ONLY":
            try:
                kw_idx = args.kwonlyargs.index(arg)
                default_val = kw_defaults[kw_idx] if kw_idx < len(kw_defaults) else None
            except:
                default_val = None
        else:
            default_val = None

        param_info = {
            "name": arg.arg,
            "kind": kind,
            "type_hint": get_type_hint(arg),
            "has_default": default_val is not None,
            "default_repr": get_default_repr(default_val) if default_val else None,
        }
        parameters.append(param_info)

    return {"parameters": parameters}


def classify_role(method_name: str, class_name):
    method_lower = method_name.lower()
    class_lower = (class_name or "").lower()

    for role, patterns in ROLE_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in method_lower:
                return role

    if "executor" in class_lower:
        return "executor"
    elif "orchestrator" in class_lower:
        return "orchestrator"
    elif "analyzer" in class_lower or "analyser" in class_lower:
        return "analyzer"
    elif "processor" in class_lower:
        return "processor"
    elif "extractor" in class_lower:
        return "extractor"
    elif "scorer" in class_lower or "scoring" in class_lower:
        return "scorer"

    if method_name.startswith("_"):
        return "utility"

    return "core"


def is_executor_method(method_name: str, class_name):
    if not class_name:
        return False
    class_lower = class_name.lower()
    return "executor" in class_lower or method_name in (
        "execute",
        "run_executor",
        "perform",
    )


def scan_file(file_path, base_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))
    except:
        return []

    relative_path = file_path.relative_to(base_path)
    module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
    module_path = ".".join(module_parts)

    scanner = CanonicalMethodScanner(module_path, str(file_path.relative_to(base_path)))
    scanner.visit(tree)

    methods = []
    for canonical_name, line_number, class_name, node in scanner.methods:
        signature = extract_signature(node)
        role = classify_role(node.name, class_name)
        is_exec = is_executor_method(node.name, class_name)

        methods.append(
            {
                "canonical_name": canonical_name,
                "file_path": str(file_path.relative_to(base_path)),
                "line_number": line_number,
                "class_name": class_name,
                "role": role,
                "is_executor": is_exec,
                "signature": signature,
            }
        )

    return methods


def scan_directory(directory):
    all_methods = []
    python_files = sorted(directory.rglob("*.py"))

    for file_path in python_files:
        methods = scan_file(file_path, directory)
        all_methods.extend(methods)

    return all_methods


def generate_excluded_methods(methods):
    excluded = {"excluded_methods": [], "exclusion_reason": "never calibrate"}

    for method in methods:
        method_name = method["canonical_name"].split(".")[-1]
        if method_name in TRIVIAL_FORMATTERS:
            excluded["excluded_methods"].append(
                {
                    "canonical_id": method["canonical_name"],
                    "reason": "trivial_formatter",
                    "method_name": method_name,
                    "file_path": method["file_path"],
                    "line_number": method["line_number"],
                }
            )
        elif method["role"] == "utility" and any(
            x in method_name.lower() for x in ["_format", "_helper", "_to_", "_from_"]
        ):
            excluded["excluded_methods"].append(
                {
                    "canonical_id": method["canonical_name"],
                    "reason": "utility_formatter",
                    "method_name": method_name,
                    "file_path": method["file_path"],
                    "line_number": method["line_number"],
                }
            )

    excluded["total_excluded"] = len(excluded["excluded_methods"])
    return excluded


def generate_statistics(methods):
    stats = {
        "total_methods": len(methods),
        "total_executors": sum(1 for m in methods if m["is_executor"]),
        "by_role": defaultdict(int),
        "by_module": defaultdict(int),
        "executor_distribution": defaultdict(int),
    }

    for method in methods:
        stats["by_role"][method["role"]] += 1
        module_name = method["canonical_name"].split(".")[0]
        stats["by_module"][module_name] += 1
        if method["is_executor"]:
            stats["executor_distribution"][module_name] += 1

    stats["by_role"] = dict(stats["by_role"])
    stats["by_module"] = dict(stats["by_module"])
    stats["executor_distribution"] = dict(stats["executor_distribution"])

    return stats


def main():
    source_dir = Path("src/farfan_pipeline")
    if not source_dir.exists():
        print(f"ERROR: {source_dir} does not exist")
        return

    print(f"Scanning {source_dir}...")
    methods = scan_directory(source_dir)
    print(f"Found {len(methods)} methods")

    methods_dict = {m["canonical_name"]: m for m in methods}

    canonical_inventory = {
        "methods": methods_dict,
        "metadata": {
            "total_methods": len(methods),
            "scan_timestamp": datetime.now(timezone.utc).isoformat(),
            "source_directory": str(source_dir),
        },
    }

    print("Writing canonical_method_inventory.json...")
    with open("canonical_method_inventory.json", "w", encoding="utf-8") as f:
        json.dump(canonical_inventory, f, indent=2, ensure_ascii=False)
    print("✓ Generated canonical_method_inventory.json")

    statistics = generate_statistics(methods)
    with open("method_statistics.json", "w", encoding="utf-8") as f:
        json.dump(statistics, f, indent=2, ensure_ascii=False)
    print("✓ Generated method_statistics.json")

    excluded = generate_excluded_methods(methods)
    with open("excluded_methods.json", "w", encoding="utf-8") as f:
        json.dump(excluded, f, indent=2, ensure_ascii=False)
    print("✓ Generated excluded_methods.json")

    print("\nSummary:")
    print(f"  Total methods: {len(methods)}")
    print(f"  Executors: {statistics['total_executors']}")
    print(f"  Excluded: {excluded['total_excluded']}")
    print(f"  Roles: {list(statistics['by_role'].keys())}")


if __name__ == "__main__":
    main()
