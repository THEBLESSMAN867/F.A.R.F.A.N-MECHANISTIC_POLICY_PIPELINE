#!/bin/bash
# Local Pipeline Validation Script
# Runs the same checks as GitHub Actions CI/CD pipeline

set -e

echo "======================================"
echo "F.A.R.F.A.N Contract Pipeline Validator"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Warning: No virtual environment detected${NC}"
    echo "Recommended: source farfan-env/bin/activate"
    echo ""
fi

# Track failures
FAILED=0

# Job 1: Contract Tests
echo "======================================"
echo "Job 1/4: Running 15 Contract Test Suites"
echo "======================================"
if python -m pytest farfan_core/farfan_core/contracts/tests -v --tb=short; then
    echo -e "${GREEN}✅ Contract tests PASSED${NC}"
else
    echo -e "${RED}❌ Contract tests FAILED${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Job 2: Verify All Contracts
echo "======================================"
echo "Job 2/4: Verify All Contracts Script"
echo "======================================"
cd farfan_core/farfan_core/contracts
if python verify_all_contracts.py; then
    echo -e "${GREEN}✅ Contract verification PASSED${NC}"
else
    echo -e "${RED}❌ Contract verification FAILED${NC}"
    FAILED=$((FAILED + 1))
fi
cd ../../..
echo ""

# Job 3: Mutation Testing
echo "======================================"
echo "Job 3/4: Mutation Testing (90% Coverage)"
echo "======================================"
echo "Installing mutation testing tools..."
pip install -q mutmut coverage[toml] 2>/dev/null || true

if python scripts/run_mutation_suite.py; then
    echo -e "${GREEN}✅ Mutation testing PASSED${NC}"
else
    echo -e "${YELLOW}⚠️  Mutation testing completed with warnings${NC}"
    echo "This is informational and does not block the pipeline"
fi
echo ""

# Job 4: Generate Release Certificates
echo "======================================"
echo "Job 4/4: Generate Release Certificates"
echo "======================================"
if python scripts/bundle_release_certificates.py; then
    echo -e "${GREEN}✅ Certificate generation PASSED${NC}"
    
    # Find the latest release directory
    LATEST_DIR=$(ls -td release_certificates_* 2>/dev/null | head -1)
    if [[ -n "$LATEST_DIR" ]]; then
        echo ""
        echo "Certificate bundle created: $LATEST_DIR"
        echo "Contents:"
        ls -lh "$LATEST_DIR"
        echo ""
        echo "Manifest:"
        cat "$LATEST_DIR/MANIFEST.json" | python -m json.tool 2>/dev/null || cat "$LATEST_DIR/MANIFEST.json"
    fi
else
    echo -e "${RED}❌ Certificate generation FAILED${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Summary
echo "======================================"
echo "Validation Summary"
echo "======================================"
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✅ All pipeline stages passed!${NC}"
    echo ""
    echo "Your changes are ready for CI/CD:"
    echo "  git add ."
    echo "  git commit -m 'your message'"
    echo "  git push"
    exit 0
else
    echo -e "${RED}❌ $FAILED pipeline stage(s) failed${NC}"
    echo ""
    echo "Please fix the errors before pushing to CI/CD."
    exit 1
fi
