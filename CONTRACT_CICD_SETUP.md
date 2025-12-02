# Contract Verification CI/CD Pipeline Setup

**Status:** ✅ Complete  
**Date:** 2024-12-01  
**Coverage Threshold:** 90%  
**Contract Count:** 15

## Overview

Fully automated continuous verification system for F.A.R.F.A.N's 15-contract governance suite, featuring:

- ✅ Automated execution of all 15 contract test suites
- ✅ Integration of `verify_all_contracts.py` into GitHub Actions
- ✅ Mutation testing via `run_mutation_suite.py` with 90% coverage threshold
- ✅ Cryptographic release certificate generation via `bundle_release_certificates.py`
- ✅ Nightly scheduled verification and archival
- ✅ Comprehensive artifact retention and audit trail

## Architecture

```
.github/workflows/
├── contract-verification.yml          # Main verification pipeline
├── contract-status-badge.yml          # Status badge generation
├── nightly-certificate-generation.yml # Nightly certificate archival
└── README.md                          # Workflow documentation

scripts/
├── run_mutation_suite.py              # Mutation testing orchestrator
├── bundle_release_certificates.py     # Certificate bundler with crypto signatures
└── validate_pipeline_locally.sh       # Local validation script

farfan_core/farfan_core/contracts/
├── tests/                             # 15 contract test suites
│   ├── test_bmc.py
│   ├── test_cdc.py
│   ├── test_context_immutability.py
│   ├── test_ffc.py
│   ├── test_idempotency.py
│   ├── test_mcc.py
│   ├── test_ot_alignment.py
│   ├── test_pic.py
│   ├── test_rc.py
│   ├── test_rcc.py
│   ├── test_refusal.py
│   ├── test_retriever_determinism.py
│   ├── test_snapshot.py
│   ├── test_toc.py
│   └── test_traceability.py
├── tools/                             # Certificate generators
└── verify_all_contracts.py            # Master verification script
```

## Workflows

### 1. Main Pipeline: `contract-verification.yml`

**Triggers:**
- Every push to `main` or `develop`
- Every pull request
- Daily at 2:00 AM UTC
- Manual dispatch

**Jobs:**

#### Job 1: Contract Tests (30 min timeout)
```yaml
- Runs all 15 test suites in parallel
- Generates JUnit XML reports
- Uploads results for 30 days
```

#### Job 2: Verify All Contracts (20 min timeout)
```yaml
- Executes verify_all_contracts.py
- Validates certificate generation
- Uploads JSON certificates for 90 days
```

#### Job 3: Mutation Testing (60 min timeout)
```yaml
- Runs mutmut on contract codebase
- Enforces 90% coverage threshold
- Generates HTML + XML coverage reports
- Uploads to Codecov
- Creates mutation report
```

#### Job 4: Generate Release Certificates (20 min timeout)
```yaml
- Only runs on main branch or manual dispatch
- Bundles all 15 certificates
- Generates cryptographic MANIFEST.json
- Creates release notes
- Retains for 365 days
```

#### Job 5: Verification Summary
```yaml
- Aggregates all job results
- Posts summary to pull requests
- Always runs (even on failure)
```

### 2. Status Badge: `contract-status-badge.yml`

**Triggers:**
- Push to main
- Contract verification completion

**Output:**
- Badge JSON for shields.io integration
- Format: `contracts | 15/15 passing | green`

### 3. Nightly Certificates: `nightly-certificate-generation.yml`

**Triggers:**
- Daily at 3:00 AM UTC
- Manual dispatch

**Jobs:**
- Generate nightly certificate bundle
- Validate historical certificate integrity
- Create health report
- Archive for 30 days

## Test Suites

All 15 contract test suites are automatically executed:

| # | Contract | Test File | Description |
|---|----------|-----------|-------------|
| 1 | Budget Monotonicity | `test_bmc.py` | Resource allocation ordering |
| 2 | Concurrency Determinism | `test_cdc.py` | Thread-safe deterministic execution |
| 3 | Context Immutability | `test_context_immutability.py` | Immutable context enforcement |
| 4 | Failure Fallback | `test_ffc.py` | Graceful degradation |
| 5 | Idempotency | `test_idempotency.py` | Duplicate detection |
| 6 | Monotone Compliance | `test_mcc.py` | Compliance monotonicity |
| 7 | Ordering & Total Alignment | `test_ot_alignment.py` | Total order consistency |
| 8 | Permutation Invariance | `test_pic.py` | Input order independence |
| 9 | Risk Certificate | `test_rc.py` | Risk scoring validation |
| 10 | Routing Contract | `test_rcc.py` | Request routing rules |
| 11 | Refusal | `test_refusal.py` | Refusal mechanism |
| 12 | Retriever Determinism | `test_retriever_determinism.py` | Deterministic retrieval |
| 13 | Snapshot | `test_snapshot.py` | State snapshot consistency |
| 14 | Total Ordering | `test_toc.py` | Complete ordering |
| 15 | Traceability | `test_traceability.py` | Audit trail validation |

## Mutation Testing

**Tool:** `mutmut`  
**Target:** `farfan_core/farfan_core/contracts/`  
**Coverage Tool:** `coverage.py` with TOML config  
**Threshold:** 90% minimum coverage

**Process:**
1. Run pytest with coverage instrumentation
2. Execute mutmut to introduce code mutations
3. Verify tests catch mutations
4. Generate detailed mutation report
5. Fail if coverage < 90%

**Reports Generated:**
- `coverage.xml` - Codecov integration
- `htmlcov/` - HTML coverage browsing
- `mutation_report.txt` - Mutation analysis

## Cryptographic Certificates

**Generator:** `scripts/bundle_release_certificates.py`

**Bundle Structure:**
```
release_certificates_YYYYMMDD_HHMMSS/
├── MANIFEST.json                      # Cryptographic manifest
├── README.md                          # Release documentation
├── bmc_certificate.json               # Budget Monotonicity
├── cdc_certificate.json               # Concurrency Determinism
├── cic_certificate.json               # Context Immutability
├── ffc_certificate.json               # Failure Fallback
├── idc_certificate.json               # Idempotency
├── mcc_certificate.json               # Monotone Compliance
├── ot_certificate.json                # Ordering & Total Alignment
├── pic_certificate.json               # Permutation Invariance
├── rc_certificate.json                # Risk Certificate
├── rcc_certificate.json               # Routing Contract
├── refc_certificate.json              # Refusal
├── rec_certificate.json               # Retriever Determinism
├── sc_certificate.json                # Snapshot
├── toc_certificate.json               # Total Ordering
└── tc_certificate.json                # Traceability
```

**MANIFEST.json Structure:**
```json
{
  "version": "1.0.0",
  "timestamp": "2024-12-01T20:00:00",
  "certificate_count": 15,
  "certificates": {
    "contract_name_certificate.json": {
      "sha256": "abc123...",
      "size_bytes": 1024
    }
  },
  "signature": "def456..."
}
```

**Signature Verification:**
```python
import json
import hashlib

with open('MANIFEST.json', 'r') as f:
    data = json.load(f)

signature = data.pop('signature')
content = json.dumps(data, sort_keys=True, indent=2)
computed = hashlib.sha256(content.encode()).hexdigest()

assert signature == computed, "Signature mismatch!"
```

## Local Development

### Quick Start
```bash
# Activate virtual environment
source farfan-env/bin/activate

# Run complete pipeline locally
./scripts/validate_pipeline_locally.sh
```

### Individual Commands

**Run all contract tests:**
```bash
python -m pytest farfan_core/farfan_core/contracts/tests -v
```

**Verify all contracts:**
```bash
cd farfan_core/farfan_core/contracts
python verify_all_contracts.py
cd ../../..
```

**Run mutation suite:**
```bash
pip install mutmut coverage[toml]
python scripts/run_mutation_suite.py
```

**Generate certificates:**
```bash
python scripts/bundle_release_certificates.py
```

**Check coverage:**
```bash
python -m pytest farfan_core/farfan_core/contracts/tests \
  --cov=farfan_core/farfan_core/contracts \
  --cov-report=html \
  --cov-fail-under=90
```

## Artifact Retention

| Artifact | Retention | Trigger |
|----------|-----------|---------|
| Contract Test Results | 30 days | Every run |
| Contract Certificates | 90 days | Every run |
| Coverage Reports | 30 days | Every run |
| Mutation Reports | 30 days | Every run |
| Release Certificates | 365 days | Main branch only |
| Nightly Certificates | 30 days | Daily |
| Health Reports | 30 days | Daily |

## Configuration

### Environment Variables

**In GitHub Actions:**
```yaml
env:
  PYTHON_VERSION: '3.12'
  COVERAGE_THRESHOLD: 90
```

**Local Override:**
```bash
export COVERAGE_THRESHOLD=85
./scripts/validate_pipeline_locally.sh
```

### Adjusting Coverage Threshold

Edit `.github/workflows/contract-verification.yml`:
```yaml
env:
  COVERAGE_THRESHOLD: 90  # Change to desired percentage
```

### Adding New Contracts

1. **Create test file:**
   ```bash
   touch farfan_core/farfan_core/contracts/tests/test_new_contract.py
   ```

2. **Create certificate generator:**
   ```bash
   touch farfan_core/farfan_core/contracts/tools/new_contract_tool.py
   ```

3. **Update expected count:**
   Edit `scripts/bundle_release_certificates.py`:
   ```python
   if len(cert_files) != 16:  # Update from 15
   ```

4. **No workflow changes needed** - automatically detected

### Schedule Modification

**Nightly tests (current: 2:00 AM UTC):**
```yaml
schedule:
  - cron: '0 2 * * *'  # Minute Hour Day Month DayOfWeek
```

**Nightly certificates (current: 3:00 AM UTC):**
```yaml
schedule:
  - cron: '0 3 * * *'
```

## Monitoring & Alerts

### GitHub Actions UI
- Navigate to **Actions** tab
- Select workflow run
- View job logs and artifacts

### Pull Request Integration
- Automated summary comments
- Status checks block merge on failure
- Coverage reports in PR view

### Codecov Integration
- Coverage trends over time
- Per-file coverage metrics
- Pull request coverage diff

### Status Badge
Add to README.md:
```markdown
![Contract Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/YOUR_ORG/YOUR_REPO/badges/contract-badge.json)
```

## Failure Handling

### Test Failures
- Pipeline fails immediately
- Blocks pull request merge
- Detailed logs in artifacts

### Coverage Below Threshold
- Mutation testing job fails
- Release certificates not generated
- Coverage report shows gaps

### Mutation Testing Issues
- Continues with warning
- Does not block pipeline
- Report available in artifacts

### Certificate Generation Errors
- Only affects main branch
- Does not block tests
- Manual retry available

## Security

### Cryptographic Integrity
- SHA-256 signatures for all certificates
- Manifest validation on every nightly run
- Historical audit trail maintained

### No Secrets Required
- Contract verification is deterministic
- No external API calls
- No authentication needed

### Artifact Security
- Read-only access via GitHub artifacts API
- Automatic expiration per retention policy
- Tamper-evident signatures

## Maintenance

### Regular Tasks
- [ ] Review nightly certificate health reports
- [ ] Monitor coverage trends
- [ ] Audit historical certificate integrity
- [ ] Update coverage threshold as needed

### Quarterly Reviews
- [ ] Validate all 15 contracts still relevant
- [ ] Review mutation testing effectiveness
- [ ] Optimize pipeline performance
- [ ] Update documentation

### When Updating Dependencies
```bash
pip install -U pytest pytest-cov mutmut coverage
pip freeze > requirements-dev.txt
```

## Troubleshooting

### "Module not found" errors
**Solution:** Check PYTHONPATH in workflow
```yaml
env:
  PYTHONPATH: farfan_core:${{ env.PYTHONPATH }}
```

### Mutation testing timeout
**Solution:** Increase timeout or reduce scope
```yaml
timeout-minutes: 90  # Increase from 60
```

### Certificate count mismatch
**Solution:** Verify all tool scripts exist
```bash
ls -1 farfan_core/farfan_core/contracts/tools/*.py | wc -l
```

### Coverage calculation errors
**Solution:** Reinstall coverage tools
```bash
pip install --force-reinstall coverage[toml] pytest-cov
```

## Compliance Checklist

✅ All 15 contract test suites automated  
✅ `verify_all_contracts.py` integrated into CI/CD  
✅ Mutation testing with 90% coverage threshold  
✅ Cryptographic release certificates generated  
✅ Nightly verification and archival  
✅ Historical audit trail maintained  
✅ Determinism validation automated  
✅ Local validation script provided  
✅ Comprehensive documentation complete  

## References

- **Workflow Documentation:** `.github/workflows/README.md`
- **Contract Suite:** `farfan_core/farfan_core/contracts/`
- **Test Files:** `farfan_core/farfan_core/contracts/tests/`
- **Governance:** `CONTRACT_GOVERNANCE.md`

## Support

For issues or questions:
1. Check workflow logs in GitHub Actions
2. Run local validation: `./scripts/validate_pipeline_locally.sh`
3. Review artifact contents
4. Consult `.github/workflows/README.md`
