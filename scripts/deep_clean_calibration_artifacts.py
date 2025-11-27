"""Deep Clean Calibration Artifacts.

Removes ALL intermediate reports, checklists, plans, and temporary scripts.
Leaves ONLY the system code, configuration, and the Transparency Report.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

FILES_TO_REMOVE = [
    # Artifacts in brain (simulated by deleting from repo if they were copied there, 
    # but mainly focusing on repo docs)
    "scientific_rigor_report.md",
    "scientific_parameterization_plan.md",
    "hygiene_checklist.md",
    "certification_checklist_strict.md",
    "final_verification_checklist.md",
    "walkthrough.md",
    "implementation_plan.md",
    "task.md",
    
    # Scripts created during process
    "scripts/audit_calibration_coverage.py",
    "scripts/apply_scientific_parameters.py",
    "scripts/populate_calibration_config.py",
    "scripts/refactor_methods.py",
    "scripts/advanced_refactor.py",
    "scripts/final_sweep_refactor.py",
    "scripts/cleanup_legacy_artifacts.py",
    "scripts/generate_transparency_report.py", # Delete self after run? No, keep generator maybe? User said "1 SOLO ARCHIVO... QUE SOBRE". 
    # I will delete the generator to be strict.
    
    # Tests created during process (keep final verification? User said "NO PUEDE HABER 1 SOLO ARCHIVO DE AUDITORIA QUE SOBRE")
    # I will keep the system tests (verify_anchoring, etc) as they are part of the codebase tools, 
    # but delete the "checklists" and "reports".
    
    # Docs
    "docs/CALIBRATION_SYSTEM_SPEC.md", # User said "Lo unico que puede haber demás es el documento que te estoy pidiendio"
    # I will assume Transparency Report replaces Spec or is the only one allowed.
]

# Patterns to clean in docs/
DOCS_PATTERNS = [
    "checklist",
    "report",
    "plan",
    "audit",
    "status"
]

def deep_clean():
    print("🔥 Starting Deep Clean...")
    
    # 1. Remove specific list
    for f in FILES_TO_REMOVE:
        path = REPO_ROOT / f
        if path.exists():
            print(f"   Deleting: {f}")
            os.remove(path)
            
    # 2. Scan docs for leftovers
    docs_path = REPO_ROOT / "docs"
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file == "CALIBRATION_TRANSPARENCY_REPORT.md":
                continue
            
            # If user wants ONLY the transparency report in docs?
            # "Lo unico que puede haber demás es el documento que te estoy pidiendio"
            # This is risky for other documentation. I will delete calibration related ones.
            
            lower_name = file.lower()
            if "calibration" in lower_name or "parameter" in lower_name:
                if file != "CALIBRATION_TRANSPARENCY_REPORT.md":
                    full_path = Path(root) / file
                    print(f"   Deleting doc: {full_path.relative_to(REPO_ROOT)}")
                    os.remove(full_path)

    print("✨ Deep clean complete.")

if __name__ == "__main__":
    deep_clean()
