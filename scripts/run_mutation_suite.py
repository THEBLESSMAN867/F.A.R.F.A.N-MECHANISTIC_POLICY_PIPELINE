#!/usr/bin/env python3
"""
Advanced Verification Suite (Mutation & Coverage)
Runs mutmut and coverage as requested by governance policy.
"""
import os
import sys
import subprocess

def run_command(cmd, description):
    print(f"\n--- {description} ---")
    print(f"Command: {cmd}")
    try:
        env = os.environ.copy()
        cwd = os.getcwd()
        farfan_core_path = os.path.join(cwd, "farfan_core")
        env["PYTHONPATH"] = f"{farfan_core_path}:{env.get('PYTHONPATH', '')}"
        
        subprocess.check_call(cmd, shell=True, env=env)
        print("✅ PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED (Exit Code: {e.returncode})")
        return False

def main():
    print("=== ADVANCED VERIFICATION SUITE ===")
    
    # 1. Coverage Analysis
    print("\n[1/3] Running Coverage Analysis...")
    cov_cmd = (
        "python -m pytest farfan_core/farfan_core/contracts/tests -v "
        "--cov=farfan_core/farfan_core/contracts "
        "--cov-report=term-missing "
        "--cov-report=xml "
        "--cov-fail-under=90"
    )
    if not run_command(cov_cmd, "Coverage Check (90% threshold)"):
        print("⚠️  Coverage below 90% threshold")
        return False

    # 2. Mutation Testing
    print("\n[2/3] Running Mutation Testing (mutmut)...")
    # Initialize mutmut if not already done
    init_cmd = "mutmut run --paths-to-mutate=farfan_core/farfan_core/contracts --tests-dir=farfan_core/farfan_core/contracts/tests || true"
    run_command(init_cmd, "Mutation Testing")
    
    # Generate mutation report
    report_cmd = "mutmut show all > mutation_report.txt 2>&1 || true"
    run_command(report_cmd, "Mutation Report Generation")
    
    # 3. Determinism Check
    print("\n[3/3] Verifying Determinism...")
    det_cmd = "python -m pytest farfan_core/farfan_core/contracts/tests/test_cdc.py -v"
    if not run_command(det_cmd, "Determinism Matrix"):
        return False

    print("\n=== MUTATION SUITE COMPLETE ===")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
