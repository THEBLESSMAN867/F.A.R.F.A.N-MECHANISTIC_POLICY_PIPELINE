# Contract CI/CD Commands Reference

Quick reference for common pipeline operations.

## 🚀 Deployment

```bash
# Stage all changes
git add .github/ scripts/ CONTRACT_CICD_*.md .gitignore

# Commit
git commit -m "Add contract verification CI/CD pipeline"

# Push to trigger pipeline
git push origin main
```

## 🧪 Local Testing

```bash
# Full pipeline validation
./scripts/validate_pipeline_locally.sh

# Individual components
python -m pytest farfan_core/farfan_core/contracts/tests -v
python farfan_core/farfan_core/contracts/verify_all_contracts.py
python scripts/run_mutation_suite.py
python scripts/bundle_release_certificates.py

# Coverage check
python -m pytest farfan_core/farfan_core/contracts/tests \
  --cov=farfan_core/farfan_core/contracts \
  --cov-report=html --cov-fail-under=90
```

## 📊 Monitoring

```bash
# List recent workflow runs
gh run list --workflow=contract-verification.yml

# View specific run
gh run view <run-id>

# Download artifacts
gh run download <run-id>

# Watch live run
gh run watch
```

## 🔧 Manual Triggers

```bash
# Trigger verification pipeline
gh workflow run contract-verification.yml

# Trigger nightly certificates
gh workflow run nightly-certificate-generation.yml

# Trigger on specific branch
gh workflow run contract-verification.yml --ref develop
```

## 📦 Artifacts

```bash
# List artifacts for a run
gh api repos/:owner/:repo/actions/runs/<run-id>/artifacts

# Download specific artifact
gh run download <run-id> --name contract-certificates

# Clean old artifacts (API)
gh api repos/:owner/:repo/actions/artifacts
```

## 🔍 Debugging

```bash
# View workflow file
cat .github/workflows/contract-verification.yml

# Validate YAML syntax
python scripts/validate_workflows.py

# Check job logs
gh run view <run-id> --log

# Check specific job
gh run view <run-id> --job=<job-id> --log
```

## 📈 Coverage

```bash
# Run with coverage
python -m pytest farfan_core/farfan_core/contracts/tests --cov

# Generate HTML report
python -m pytest farfan_core/farfan_core/contracts/tests \
  --cov=farfan_core/farfan_core/contracts --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 🧬 Mutation Testing

```bash
# Run mutation tests
mutmut run --paths-to-mutate=farfan_core/farfan_core/contracts

# Show results
mutmut results

# Show specific mutation
mutmut show <mutation-id>

# Generate report
mutmut results > mutation_report.txt
```

## 🔐 Certificate Validation

```bash
# Generate certificates
python scripts/bundle_release_certificates.py

# Find latest bundle
ls -td release_certificates_* | head -1

# Verify manifest signature
python -c "
import json, hashlib
data = json.load(open('release_certificates_*/MANIFEST.json'))
sig = data.pop('signature')
computed = hashlib.sha256(json.dumps(data, sort_keys=True, indent=2).encode()).hexdigest()
print('✅ Valid' if sig == computed else '❌ Invalid')
"
```

## 🔄 Workflow Management

```bash
# Enable workflow
gh workflow enable contract-verification.yml

# Disable workflow
gh workflow disable contract-verification.yml

# View workflow details
gh workflow view contract-verification.yml

# List all workflows
gh workflow list
```

## 📝 Status Checks

```bash
# Check status of latest run
gh run list --workflow=contract-verification.yml --limit 1

# Check PR status checks
gh pr checks <pr-number>

# View PR with checks
gh pr view <pr-number> --web
```

## 🛠️ Configuration

```bash
# View environment variables
gh api repos/:owner/:repo/actions/variables

# Set environment variable (requires permissions)
gh variable set COVERAGE_THRESHOLD --body "90"

# View secrets (names only)
gh secret list
```

## 🔢 Statistics

```bash
# Count test files
ls -1 farfan_core/farfan_core/contracts/tests/test_*.py | wc -l

# Count tool scripts
ls -1 farfan_core/farfan_core/contracts/tools/*.py | wc -l

# Count certificate files
ls -1 *_certificate.json 2>/dev/null | wc -l

# Workflow file sizes
wc -l .github/workflows/*.yml
```

## 🐛 Troubleshooting

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify contract module
python -c "import farfan_core.contracts; print('✅ OK')"

# Test single contract
python -m pytest farfan_core/farfan_core/contracts/tests/test_bmc.py -v

# Run with verbose output
python -m pytest farfan_core/farfan_core/contracts/tests -vv --tb=long
```

## 📚 Documentation

```bash
# View README files
cat .github/workflows/README.md
cat CONTRACT_CICD_QUICKSTART.md
cat CONTRACT_CICD_SETUP.md
cat CONTRACT_CICD_CHECKLIST.md

# Generate documentation site (if using MkDocs)
mkdocs serve
```

## 🔄 Update Dependencies

```bash
# Update requirements
pip install -U pytest pytest-cov mutmut coverage
pip freeze > requirements-dev.txt

# Update GitHub Actions
# (Check .github/workflows/*.yml for updates)
```

## 📊 Metrics

```bash
# Line counts
find .github/workflows -name "*.yml" -exec wc -l {} +
find scripts -name "validate*.py" -o -name "*mutation*.py" -exec wc -l {} +

# File counts
find .github/workflows -type f | wc -l
find farfan_core/farfan_core/contracts/tests -name "test_*.py" | wc -l
```

## 🎯 Quick Checks

```bash
# Is everything committed?
git status --short

# Are workflows valid?
python scripts/validate_workflows.py

# Can tests run?
python -m pytest farfan_core/farfan_core/contracts/tests --collect-only

# Are scripts executable?
ls -l scripts/*.sh scripts/*.py | grep "^-rwx"
```

## 💡 Tips

- Use `gh` CLI for faster GitHub Actions interaction
- Run `./scripts/validate_pipeline_locally.sh` before every push
- Check Actions tab immediately after pushing
- Download artifacts to verify certificate generation
- Monitor coverage trends over time
- Review mutation reports for test quality insights

## 🆘 Help

```bash
# GitHub CLI help
gh help
gh workflow help
gh run help

# Pytest help
pytest --help
pytest --markers

# Coverage help
coverage help
```
