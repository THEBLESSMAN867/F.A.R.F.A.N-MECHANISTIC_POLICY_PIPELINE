# Contract Verification CI/CD Pipeline

Automated continuous verification system for F.A.R.F.A.N's 15-contract suite with mutation testing and cryptographic certificate generation.

## Workflows

### 1. Contract Verification Pipeline (`contract-verification.yml`)

**Primary verification workflow** that runs on every push, PR, and nightly schedule.

**Jobs:**
- **contract-tests**: Executes all 15 contract test suites in parallel
- **verify-all-contracts**: Runs `verify_all_contracts.py` to validate certificates
- **mutation-testing**: Executes mutation testing suite with 90% coverage threshold
- **generate-release-certificates**: Bundles cryptographic release certificates
- **contract-verification-summary**: Generates comprehensive status report

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch
- Nightly at 2:00 AM UTC

**Artifacts:**
- `contract-test-results`: JUnit XML test results (30 days)
- `contract-certificates`: JSON certificates for all contracts (90 days)
- `coverage-report`: HTML coverage report (30 days)
- `mutation-report`: Mutation testing results (30 days)
- `release-certificates-{SHA}`: Cryptographic certificate bundle (365 days)

**Coverage Threshold:** 90% (configurable via `COVERAGE_THRESHOLD` env var)

### 2. Contract Status Badge (`contract-status-badge.yml`)

Generates status badge showing contract verification state.

**Triggers:**
- Push to `main` branch
- Completion of Contract Verification Pipeline

**Output:** JSON badge data for shields.io integration

### 3. Nightly Certificate Generation (`nightly-certificate-generation.yml`)

Automated nightly certificate generation and archival.

**Triggers:**
- Daily at 3:00 AM UTC
- Manual workflow dispatch

**Jobs:**
- **generate-certificates**: Creates nightly certificate bundle
- **validate-historical-certificates**: Validates integrity of historical certificates

**Artifacts:**
- `nightly-certificates-{DATE}`: Daily certificate snapshot (30 days)
- `health-report-{DATE}`: System health report (30 days)

## Test Suites Covered

The pipeline automatically runs all 15 contract test suites:

1. **test_bmc.py** - Budget Monotonicity Contract
2. **test_cdc.py** - Concurrency Determinism Contract
3. **test_context_immutability.py** - Context Immutability Contract
4. **test_ffc.py** - Failure Fallback Contract
5. **test_idempotency.py** - Idempotency & Deduplication Contract
6. **test_mcc.py** - Monotone Compliance Contract
7. **test_ot_alignment.py** - Ordering & Total Alignment Contract
8. **test_pic.py** - Permutation Invariance Contract
9. **test_rc.py** - Risk Certificate Contract
10. **test_rcc.py** - Routing Contract
11. **test_refusal.py** - Refusal Contract
12. **test_retriever_determinism.py** - Retriever Determinism Contract
13. **test_snapshot.py** - Snapshot Contract
14. **test_toc.py** - Total Ordering Contract
15. **test_traceability.py** - Traceability Contract

## Mutation Testing

Mutation testing is performed using `mutmut` with the following configuration:

- **Target:** `farfan_core/farfan_core/contracts/`
- **Tests:** `farfan_core/farfan_core/contracts/tests/`
- **Threshold:** 90% coverage required
- **Reports:** Generated as `mutation_report.txt`

## Cryptographic Certificates

Release certificates include:

- **Individual Certificates**: JSON files for each contract
- **MANIFEST.json**: Cryptographic manifest with SHA-256 signatures
- **README.md**: Release documentation
- **Signature Verification**: Automated integrity validation

### Certificate Structure

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

## Local Execution

### Run All Tests
```bash
python -m pytest farfan_core/farfan_core/contracts/tests -v
```

### Verify All Contracts
```bash
cd farfan_core/farfan_core/contracts
python verify_all_contracts.py
```

### Run Mutation Suite
```bash
python scripts/run_mutation_suite.py
```

### Generate Release Certificates
```bash
python scripts/bundle_release_certificates.py
```

## Environment Variables

- `PYTHON_VERSION`: Python version (default: 3.12)
- `COVERAGE_THRESHOLD`: Minimum coverage % (default: 90)

## Failure Handling

- Tests continue even if mutation testing fails
- Coverage threshold failures block release certificate generation
- All artifacts are uploaded regardless of job status (using `if: always()`)
- Historical certificate validation runs independently

## Integration with Main Pipeline

This contract verification pipeline integrates with the main F.A.R.F.A.N build pipeline:

1. Runs independently on contract changes
2. Blocks merges if contracts fail
3. Generates certificates only for `main` branch
4. Provides coverage reports to Codecov

## Maintenance

### Adding New Contracts

1. Create test file in `farfan_core/farfan_core/contracts/tests/test_*.py`
2. Create certificate generator in `farfan_core/farfan_core/contracts/tools/*.py`
3. Update expected count in `bundle_release_certificates.py` (currently: 15)
4. No workflow changes required - automatically detected

### Adjusting Coverage Threshold

Edit `COVERAGE_THRESHOLD` in `contract-verification.yml`:

```yaml
env:
  COVERAGE_THRESHOLD: 90  # Adjust as needed
```

### Modifying Schedule

Edit cron expressions:
- `contract-verification.yml`: Line 8 (nightly tests)
- `nightly-certificate-generation.yml`: Line 3 (certificate generation)

## Monitoring

- **GitHub Actions UI**: View workflow runs and artifacts
- **Pull Request Comments**: Automated verification summaries
- **Badges**: Contract status badge (via `contract-status-badge.yml`)
- **Codecov**: Coverage tracking and trends

## Security

- All certificates include SHA-256 cryptographic signatures
- Manifest integrity validated on every nightly run
- Historical certificates archived for audit trail
- No secrets required for contract verification

## Compliance

Adheres to F.A.R.F.A.N governance requirements:

✅ 15-contract suite execution  
✅ Mutation testing with 90% threshold  
✅ Cryptographic certificate generation  
✅ Automated verification on every commit  
✅ Historical audit trail  
✅ Determinism validation  

## Support

For issues with the pipeline:
1. Check workflow logs in GitHub Actions UI
2. Review artifact contents (test results, coverage reports)
3. Run verification scripts locally to reproduce
4. Verify PYTHONPATH configuration in failing jobs
