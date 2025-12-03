#!/usr/bin/env python3
"""
Method Inventory Scanner

Recursively scans src/farfan_pipeline/ to extract all top-level functions and
class methods (excluding nested inner functions). Captures module path, class name,
method name, signature details, line numbers, and builds canonical IDs.

Output format: List of method records with:
- module_path: Dot-separated module path (e.g., 'farfan_pipeline.core.orchestrator.core')
- class_name: Class name if method is in a class, else None
- method_name: Function/method name
- signature: Dict with parameters (name, default, type_hint, kind)
- line_number: Starting line number in source file
- canonical_id: Full identifier ('module.Class.method' or 'module.function')
- file_path: Relative path from repo root
"""

import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class MethodParameter:
    name: str
    kind: str
    default: str | None = None
    type_hint: str | None = None


@dataclass
class MethodRecord:
    module_path: str
    method_name: str
    signature: list[dict[str, str | None]]
    line_number: int
    canonical_id: str
    file_path: str
    class_name: str | None = None


class MethodInventoryScanner(ast.NodeVisitor):
    def __init__(self, module_path: str, file_path: str):
        self.module_path = module_path
        self.file_path = file_path
        self.methods: list[MethodRecord] = []
        self.current_class: str | None = None
        self.depth = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        previous_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._process_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._process_function(node)

    def _process_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if self.depth > 0:
            return

        self.depth += 1

        params = self._extract_parameters(node)

        if self.current_class:
            canonical_id = f"{self.module_path}.{self.current_class}.{node.name}"
        else:
            canonical_id = f"{self.module_path}.{node.name}"

        record = MethodRecord(
            module_path=self.module_path,
            class_name=self.current_class,
            method_name=node.name,
            signature=[asdict(p) for p in params],
            line_number=node.lineno,
            canonical_id=canonical_id,
            file_path=self.file_path,
        )

        self.methods.append(record)

        self.generic_visit(node)
        self.depth -= 1

    def _extract_parameters(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> list[MethodParameter]:
        params: list[MethodParameter] = []
        args = node.args

        def get_type_hint(annotation: ast.expr | None) -> str | None:
            if annotation is None:
                return None
            return ast.unparse(annotation)

        def get_default(default: ast.expr | None) -> str | None:
            if default is None:
                return None
            try:
                return ast.unparse(default)
            except Exception:
                return "<complex_default>"

        all_args = args.posonlyargs + args.args
        defaults_offset = len(all_args) - len(args.defaults)

        for i, arg in enumerate(all_args):
            default_value = None
            if i >= defaults_offset:
                default_value = get_default(args.defaults[i - defaults_offset])

            kind = "positional_or_keyword"
            if i < len(args.posonlyargs):
                kind = "positional_only"

            params.append(
                MethodParameter(
                    name=arg.arg,
                    kind=kind,
                    default=default_value,
                    type_hint=get_type_hint(arg.annotation),
                )
            )

        if args.vararg:
            params.append(
                MethodParameter(
                    name=args.vararg.arg,
                    kind="var_positional",
                    type_hint=get_type_hint(args.vararg.annotation),
                )
            )

        for arg in args.kwonlyargs:
            default_value = None
            for i, kw_arg in enumerate(args.kwonlyargs):
                if kw_arg.arg == arg.arg and i < len(args.kw_defaults):
                    default_value = get_default(args.kw_defaults[i])
                    break

            params.append(
                MethodParameter(
                    name=arg.arg,
                    kind="keyword_only",
                    default=default_value,
                    type_hint=get_type_hint(arg.annotation),
                )
            )

        if args.kwarg:
            params.append(
                MethodParameter(
                    name=args.kwarg.arg,
                    kind="var_keyword",
                    type_hint=get_type_hint(args.kwarg.annotation),
                )
            )

        return params


def scan_file(file_path: Path, repo_root: Path) -> list[MethodRecord]:
    relative_path = file_path.relative_to(repo_root)

    parts = relative_path.with_suffix("").parts
    if parts[0] == "src":
        parts = parts[1:]

    module_path = ".".join(parts)

    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return []

    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        print(f"Warning: Syntax error in {file_path}: {e}", file=sys.stderr)
        return []

    scanner = MethodInventoryScanner(module_path, str(relative_path))
    scanner.visit(tree)

    return scanner.methods


def scan_directory(directory: Path, repo_root: Path) -> list[MethodRecord]:
    all_methods: list[MethodRecord] = []

    python_files = sorted(directory.rglob("*.py"))

    for py_file in python_files:
        methods = scan_file(py_file, repo_root)
        all_methods.extend(methods)

    return all_methods


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    source_dir = repo_root / "src" / "farfan_pipeline"

    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {source_dir}...", file=sys.stderr)

    methods = scan_directory(source_dir, repo_root)

    print(f"Found {len(methods)} methods", file=sys.stderr)

    output = {
        "metadata": {
            "total_methods": len(methods),
            "source_directory": str(source_dir.relative_to(repo_root)),
        },
        "methods": [asdict(m) for m in methods],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
