#!/usr/bin/env python3
"""
Comprehensive Hardcoding Audit Scanner

Detects calibration hardcoding violations:
1. Calibration values (scores, weights, thresholds, coefficients) in .py files
2. Inline JSON/dict literals containing calibration data
3. YAML file references (prohibited format)
4. Undeclared Bayesian priors

Generates violations_audit.md with file/line/code context.
"""

import ast
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class Violation:
    """Represents a hardcoding violation."""
    file_path: str
    line_number: int
    violation_type: str
    code_snippet: str
    context: str = ""
    severity: str = "HIGH"


@dataclass
class AuditResult:
    """Results of hardcoding audit."""
    violations: List[Violation] = field(default_factory=list)
    files_scanned: int = 0
    yaml_references: Set[str] = field(default_factory=set)
    
    def add_violation(self, v: Violation) -> None:
        self.violations.append(v)
    
    def get_by_type(self, vtype: str) -> List[Violation]:
        return [v for v in self.violations if v.violation_type == vtype]


class CalibrationHardcodingDetector(ast.NodeVisitor):
    """AST visitor to detect hardcoded calibration values."""
    
    CALIBRATION_KEYWORDS = {
        'score', 'weight', 'threshold', 'coefficient', 'alpha', 'beta', 'gamma',
        'b_theory', 'b_impl', 'b_deploy', 'prior', 'posterior', 'likelihood',
        'calibration', 'layer', 'choquet', 'intrinsic', 'runtime',
        'w_th', 'w_imp', 'w_dep', 'g_function', 'sigmoidal_k', 'sigmoidal_x0',
        'abort_threshold', 'compatibility_level', 'alignment', 'default_score'
    }
    
    CALIBRATION_PATTERNS = [
        r'\b(score|weight|threshold|coefficient)\s*[=:]\s*[0-9.]+',
        r'b_(theory|impl|deploy)\s*[=:]\s*[0-9.]+',
        r'(alpha|beta|gamma|prior)\s*[=:]\s*[0-9.]+',
        r'@(b|chain|q|d|p|C|u|m)\s*[=:]\s*[0-9.]+',
    ]
    
    def __init__(self, file_path: str, source_lines: List[str]):
        self.file_path = file_path
        self.source_lines = source_lines
        self.violations: List[Violation] = []
        self.in_dict_context = False
        self.dict_depth = 0
        
    def visit_Assign(self, node: ast.Assign) -> None:
        """Detect hardcoded values in assignments."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                
                # Check if variable name suggests calibration
                if any(kw in var_name for kw in self.CALIBRATION_KEYWORDS):
                    if isinstance(node.value, ast.Constant):
                        if isinstance(node.value.value, (int, float)):
                            self._add_violation(
                                node.lineno,
                                "HARDCODED_CALIBRATION_VALUE",
                                f"Variable '{target.id}' assigned hardcoded value: {node.value.value}",
                                "HIGH"
                            )
                    elif isinstance(node.value, ast.Dict):
                        self._add_violation(
                            node.lineno,
                            "INLINE_CALIBRATION_DICT",
                            f"Variable '{target.id}' assigned inline dict literal",
                            "HIGH"
                        )
        
        self.generic_visit(node)
    
    def visit_Dict(self, node: ast.Dict) -> None:
        """Detect inline dict literals with calibration data."""
        self.dict_depth += 1
        
        # Check if dict contains calibration keywords in keys
        has_calibration_keys = False
        calibration_keys = []
        
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                key_lower = key.value.lower()
                if any(kw in key_lower for kw in self.CALIBRATION_KEYWORDS):
                    has_calibration_keys = True
                    calibration_keys.append(key.value)
        
        if has_calibration_keys and self.dict_depth <= 2:
            # Only flag top-level or shallow dicts to avoid false positives
            self._add_violation(
                node.lineno,
                "INLINE_CALIBRATION_DICT",
                f"Dict literal contains calibration keys: {', '.join(calibration_keys[:3])}",
                "HIGH"
            )
        
        self.generic_visit(node)
        self.dict_depth -= 1
    
    def visit_Call(self, node: ast.Call) -> None:
        """Detect json.loads() with inline JSON or undeclared priors."""
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'loads' and isinstance(node.func.value, ast.Name):
                if node.func.value.id == 'json':
                    # Check if json.loads is called with string literal
                    if node.args and isinstance(node.args[0], ast.Constant):
                        if isinstance(node.args[0].value, str):
                            content = node.args[0].value.lower()
                            if any(kw in content for kw in self.CALIBRATION_KEYWORDS):
                                self._add_violation(
                                    node.lineno,
                                    "INLINE_JSON_CALIBRATION",
                                    "json.loads() called with inline JSON containing calibration data",
                                    "CRITICAL"
                                )
        
        # Detect Bayesian prior declarations
        if isinstance(node.func, ast.Name):
            func_name = node.func.id.lower()
            if 'prior' in func_name or 'beta' in func_name or 'gamma' in func_name or 'dirichlet' in func_name:
                # Check if it's from scipy.stats or similar
                self._add_violation(
                    node.lineno,
                    "UNDECLARED_BAYESIAN_PRIOR",
                    f"Potential undeclared Bayesian prior: {node.func.id}()",
                    "MEDIUM"
                )
        
        self.generic_visit(node)
    
    def visit_Constant(self, node: ast.Constant) -> None:
        """Detect numeric constants in suspicious contexts."""
        if isinstance(node.value, (int, float)):
            # Check if the constant is in typical calibration range
            if 0.0 <= node.value <= 1.0 or 0 <= node.value <= 100:
                # Get parent context to determine if it's suspicious
                # This is simplified; full implementation would track parent nodes
                pass
        
        self.generic_visit(node)
    
    def _add_violation(self, line_no: int, vtype: str, context: str, severity: str) -> None:
        """Add a violation to the list."""
        code_snippet = self._get_code_snippet(line_no)
        
        self.violations.append(Violation(
            file_path=self.file_path,
            line_number=line_no,
            violation_type=vtype,
            code_snippet=code_snippet,
            context=context,
            severity=severity
        ))
    
    def _get_code_snippet(self, line_no: int, context_lines: int = 2) -> str:
        """Get code snippet with context."""
        start = max(0, line_no - context_lines - 1)
        end = min(len(self.source_lines), line_no + context_lines)
        
        lines = []
        for i in range(start, end):
            marker = ">>>" if i == line_no - 1 else "   "
            lines.append(f"{marker} {i+1:4d}: {self.source_lines[i].rstrip()}")
        
        return "\n".join(lines)


class RegexCalibrationScanner:
    """Regex-based scanner for patterns AST might miss."""
    
    PATTERNS = [
        # Hardcoded numeric assignments to calibration variables
        (r'(\w*(?:score|weight|threshold|coefficient)\w*)\s*[=:]\s*([0-9.]+)',
         'HARDCODED_CALIBRATION_VALUE'),
        
        # Inline calibration dicts
        (r'(?:intrinsic|runtime|layer).*?\{.*?["\'](?:score|weight|threshold)["\'].*?\}',
         'INLINE_CALIBRATION_DICT'),
        
        # YAML references
        (r'\.ya?ml["\']?',
         'YAML_REFERENCE'),
        
        # @b, @chain, etc. with values
        (r'@(?:b|chain|q|d|p|C|u|m)\s*[=:]\s*([0-9.]+)',
         'HARDCODED_LAYER_SCORE'),
        
        # Bayesian priors
        (r'(?:scipy\.stats\.|pymc3\.|pymc\.)(?:beta|gamma|normal|dirichlet)\s*\(',
         'UNDECLARED_BAYESIAN_PRIOR'),
        
        # Choquet weights
        (r'choquet.*?(?:weight|coefficient)s?\s*[=:]\s*[\[{]',
         'HARDCODED_CHOQUET_WEIGHTS'),
    ]
    
    def scan_file(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        """Scan file content with regex patterns."""
        violations = []
        
        for pattern, vtype in self.PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE | re.DOTALL):
                # Find line number
                line_no = content[:match.start()].count('\n') + 1
                
                # Get code snippet
                start = max(0, line_no - 3)
                end = min(len(lines), line_no + 2)
                snippet_lines = []
                for i in range(start, end):
                    marker = ">>>" if i == line_no - 1 else "   "
                    snippet_lines.append(f"{marker} {i+1:4d}: {lines[i].rstrip()}")
                snippet = "\n".join(snippet_lines)
                
                violations.append(Violation(
                    file_path=file_path,
                    line_number=line_no,
                    violation_type=vtype,
                    code_snippet=snippet,
                    context=f"Pattern matched: {match.group(0)[:80]}",
                    severity="HIGH" if vtype in ['YAML_REFERENCE', 'INLINE_CALIBRATION_DICT'] else "MEDIUM"
                ))
        
        return violations


def scan_python_file(file_path: Path) -> List[Violation]:
    """Scan a Python file for hardcoding violations."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        violations = []
        
        # AST-based detection
        try:
            tree = ast.parse(content, filename=str(file_path))
            detector = CalibrationHardcodingDetector(str(file_path), lines)
            detector.visit(tree)
            violations.extend(detector.violations)
        except SyntaxError as e:
            violations.append(Violation(
                file_path=str(file_path),
                line_number=e.lineno or 0,
                violation_type="PARSE_ERROR",
                code_snippet=f"Syntax error: {e}",
                severity="LOW"
            ))
        
        # Regex-based detection
        regex_scanner = RegexCalibrationScanner()
        violations.extend(regex_scanner.scan_file(str(file_path), content, lines))
        
        return violations
    
    except Exception as e:
        return [Violation(
            file_path=str(file_path),
            line_number=0,
            violation_type="SCAN_ERROR",
            code_snippet=f"Error scanning file: {e}",
            severity="LOW"
        )]


def scan_directory(root_path: Path, include_patterns: List[str] = None) -> AuditResult:
    """Scan directory tree for violations."""
    if include_patterns is None:
        include_patterns = ['src/farfan_pipeline/**/*.py']
    
    result = AuditResult()
    
    # Collect all Python files
    python_files = []
    for pattern in include_patterns:
        python_files.extend(root_path.glob(pattern))
    
    # Scan each file
    for py_file in python_files:
        if py_file.is_file():
            result.files_scanned += 1
            violations = scan_python_file(py_file)
            result.violations.extend(violations)
            
            # Check for YAML references
            yaml_viols = [v for v in violations if v.violation_type == 'YAML_REFERENCE']
            if yaml_viols:
                result.yaml_references.add(str(py_file))
    
    return result


def generate_markdown_report(result: AuditResult, output_path: Path) -> None:
    """Generate violations_audit.md report."""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Calibration Hardcoding Audit Report\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"- **Files Scanned**: {result.files_scanned}\n")
        f.write(f"- **Total Violations**: {len(result.violations)}\n")
        f.write(f"- **CRITICAL Violations**: {len([v for v in result.violations if v.severity == 'CRITICAL'])}\n")
        f.write(f"- **HIGH Violations**: {len([v for v in result.violations if v.severity == 'HIGH'])}\n")
        f.write(f"- **MEDIUM Violations**: {len([v for v in result.violations if v.severity == 'MEDIUM'])}\n")
        f.write(f"- **Files with YAML References**: {len(result.yaml_references)}\n\n")
        
        # Violation categories
        f.write("## Violation Categories\n\n")
        
        violation_types = {}
        for v in result.violations:
            violation_types.setdefault(v.violation_type, []).append(v)
        
        for vtype in sorted(violation_types.keys()):
            f.write(f"### {vtype.replace('_', ' ').title()} ({len(violation_types[vtype])} occurrences)\n\n")
        
        # Known Violators Section
        f.write("## Known Violators (Priority Review)\n\n")
        
        known_violators = [
            'src/farfan_pipeline/core/calibration/orchestrator.py',
            'src/farfan_pipeline/core/calibration/layer_computers.py'
        ]
        
        for known_file in known_violators:
            f.write(f"### {known_file}\n\n")
            file_violations = [v for v in result.violations if known_file in v.file_path]
            
            if file_violations:
                for v in sorted(file_violations, key=lambda x: x.line_number):
                    f.write(f"**Line {v.line_number}** - `{v.violation_type}` [{v.severity}]\n\n")
                    f.write(f"*Context*: {v.context}\n\n")
                    f.write("```python\n")
                    f.write(v.code_snippet)
                    f.write("\n```\n\n")
            else:
                f.write("*No violations detected (may require manual review)*\n\n")
        
        # All Violations by File
        f.write("## Detailed Violations by File\n\n")
        
        violations_by_file = {}
        for v in result.violations:
            violations_by_file.setdefault(v.file_path, []).append(v)
        
        for file_path in sorted(violations_by_file.keys()):
            # Skip known violators (already covered)
            if any(kv in file_path for kv in known_violators):
                continue
            
            f.write(f"### {file_path}\n\n")
            file_viols = violations_by_file[file_path]
            f.write(f"**{len(file_viols)} violation(s)**\n\n")
            
            for v in sorted(file_viols, key=lambda x: x.line_number):
                f.write(f"#### Line {v.line_number} - `{v.violation_type}` [{v.severity}]\n\n")
                if v.context:
                    f.write(f"*{v.context}*\n\n")
                f.write("```python\n")
                f.write(v.code_snippet)
                f.write("\n```\n\n")
        
        # YAML References
        if result.yaml_references:
            f.write("## YAML File References (PROHIBITED)\n\n")
            f.write("**CRITICAL**: YAML is a prohibited format for calibration data.\n\n")
            for yaml_file in sorted(result.yaml_references):
                f.write(f"- {yaml_file}\n")
            f.write("\n")
        
        # Recommendations
        f.write("## Remediation Recommendations\n\n")
        f.write("1. **Move all calibration values to JSON config files**:\n")
        f.write("   - `config/intrinsic_calibration.json` for @b scores\n")
        f.write("   - `config/contextual_parametrization.json` for layer parameters\n\n")
        
        f.write("2. **Remove inline dict/JSON literals**:\n")
        f.write("   - Load all calibration data via `IntrinsicCalibrationLoader`\n")
        f.write("   - Use `CalibrationOrchestrator` as single entry point\n\n")
        
        f.write("3. **Eliminate YAML references**:\n")
        f.write("   - Convert any YAML files to JSON\n")
        f.write("   - Update all file references\n\n")
        
        f.write("4. **Declare Bayesian priors explicitly**:\n")
        f.write("   - Document all priors in calibration config\n")
        f.write("   - Add prior justification comments\n\n")
        
        f.write("5. **Use CalibrationOrchestrator exclusively**:\n")
        f.write("   - Remove direct score computations\n")
        f.write("   - Route all calibration through `calibrate_method()`\n\n")


def main():
    """Main entry point."""
    root = Path.cwd()
    
    print("=" * 80)
    print("FARFAN Calibration Hardcoding Audit Scanner")
    print("=" * 80)
    print()
    
    print("Scanning Python files for calibration hardcoding violations...")
    print()
    
    # Scan directory
    result = scan_directory(root)
    
    print(f"Scanned {result.files_scanned} files")
    print(f"Found {len(result.violations)} violations")
    print()
    
    # Generate report
    output_path = root / "violations_audit.md"
    generate_markdown_report(result, output_path)
    
    print(f"Report generated: {output_path}")
    print()
    
    # Summary by severity
    critical = len([v for v in result.violations if v.severity == 'CRITICAL'])
    high = len([v for v in result.violations if v.severity == 'HIGH'])
    medium = len([v for v in result.violations if v.severity == 'MEDIUM'])
    
    print("Violations by Severity:")
    print(f"  CRITICAL: {critical}")
    print(f"  HIGH:     {high}")
    print(f"  MEDIUM:   {medium}")
    print()
    
    # Known violators
    print("Known Violator Files:")
    for known in ['orchestrator.py', 'layer_computers.py']:
        count = len([v for v in result.violations if known in v.file_path])
        print(f"  {known}: {count} violations")
    print()
    
    if result.yaml_references:
        print(f"⚠️  CRITICAL: {len(result.yaml_references)} files reference YAML (prohibited format)")
        print()
    
    print("=" * 80)
    print(f"Audit complete. Review {output_path} for details.")
    print("=" * 80)
    
    # Exit with error code if critical violations found
    if critical > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
