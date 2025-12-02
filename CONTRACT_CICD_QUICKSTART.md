# Contract CI/CD Pipeline - Quick Start Guide

## 🚀 What's Been Set Up

A complete CI/CD pipeline for F.A.R.F.A.N's 15-contract verification suite with:
- ✅ Automated test execution
- ✅ 90% coverage threshold enforcement
- ✅ Mutation testing
- ✅ Cryptographic certificate generation

## 📁 Files Added/Modified

### New Files
```
.github/workflows/
├── contract-verification.yml           # Main pipeline
├── contract-status-badge.yml           # Status badge
├── nightly-certificate-generation.yml  # Nightly archival
└── README.md                           # Workflow docs

scripts/
├── validate_pipeline_locally.sh        # Local validation
└── validate_workflows.py               # YAML validator

CONTRACT_CICD_SETUP.md                  # Complete documentation
CONTRACT_CICD_CHECKLIST.md             # Implementation checklist
CONTRACT_CICD_QUICKSTART.md            # This file
```

### Modified Files
```
scripts/run_mutation_suite.py           # Updated paths
scripts/bundle_release_certificates.py  # Added crypto signatures
.gitignore                              # Added artifact exclusions
```

## 🔧 Local Testing (Before Push)

```bash
# Run complete validation
./scripts/validate_pipeline_locally.sh

# Or run individual steps:
python -m pytest farfan_core/farfan_core/contracts/tests -v
cd farfan_core/farfan_core/contracts && python verify_all_contracts.py
python scripts/run_mutation_suite.py
python scripts/bundle_release_certificates.py
```

## 📤 Deployment Steps

```bash
# 1. Stage all changes
git add .github/workflows/ scripts/ CONTRACT_CICD_*.md .gitignore

# 2. Commit
git commit -m "Add contract verification CI/CD pipeline

- Automate execution of all 15 contract test suites
- Integrate verify_all_contracts.py into GitHub Actions
- Add mutation testing with 90% coverage threshold
- Generate cryptographic release certificates
- Add nightly verification and archival"

# 3. Push
git push origin main
```

## 📊 Monitoring After Deployment

1. **GitHub Actions Tab:**
   - Navigate to repository → Actions
   - Watch "Contract Verification Pipeline" workflow
   - First run should trigger automatically

2. **View Artifacts:**
   - Click on workflow run
   - Scroll to "Artifacts" section
   - Download test results, certificates, coverage reports

3. **Check Pull Requests:**
   - Future PRs will show status checks
   - Automated summary comment will be posted

## 🎯 What Happens Automatically

### On Every Push/PR
- ✅ Run all 15 contract tests
- ✅ Execute verify_all_contracts.py
- ✅ Run mutation testing (90% coverage)
- ✅ Generate coverage reports
- ✅ Post PR summary comments

### On Main Branch Only
- ✅ Generate release certificates
- ✅ Create cryptographic manifest
- ✅ Archive for 365 days

### Nightly (3 AM UTC)
- ✅ Generate certificate snapshot
- ✅ Validate historical integrity
- ✅ Create health report

## 📈 Key Metrics

- **Test Suites:** 15 contracts
- **Coverage Threshold:** 90%
- **Artifact Retention:** 30-365 days
- **Pipeline Timeout:** 30-60 min per job

## 🔍 Troubleshooting

**Pipeline fails?**
```bash
# Run locally first
./scripts/validate_pipeline_locally.sh
```

**Coverage below 90%?**
```bash
python -m pytest farfan_core/farfan_core/contracts/tests \
  --cov=farfan_core/farfan_core/contracts \
  --cov-report=html
# Open htmlcov/index.html
```

**Need help?**
- Check `.github/workflows/README.md`
- Review `CONTRACT_CICD_SETUP.md`
- Examine workflow logs in GitHub Actions UI

## 📚 Documentation

- **Complete Setup:** `CONTRACT_CICD_SETUP.md`
- **Implementation Details:** `CONTRACT_CICD_CHECKLIST.md`
- **Workflow Docs:** `.github/workflows/README.md`
- **Local Validation:** `scripts/validate_pipeline_locally.sh`

## ✅ Ready to Deploy

All files are prepared and tested. Execute the deployment steps above to activate the CI/CD pipeline!
