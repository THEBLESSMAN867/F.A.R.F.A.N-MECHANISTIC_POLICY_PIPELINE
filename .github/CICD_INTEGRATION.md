# CI/CD Integration Guide

## GitHub Actions Badge

Add this badge to your main README.md to show contract verification status:

```markdown
![Contract Verification](https://github.com/{YOUR_ORG}/{YOUR_REPO}/workflows/Contract%20Verification%20Pipeline/badge.svg)
```

Replace `{YOUR_ORG}` and `{YOUR_REPO}` with your GitHub organization and repository names.

## Codecov Integration (Optional)

To enable coverage tracking:

1. **Add Codecov to your repository:**
   - Visit https://codecov.io
   - Sign in with GitHub
   - Add your repository

2. **Add secret to GitHub:**
   - Repository Settings → Secrets → Actions
   - Add `CODECOV_TOKEN` from Codecov dashboard

3. **Badge for README:**
   ```markdown
   ![Coverage](https://codecov.io/gh/{YOUR_ORG}/{YOUR_REPO}/branch/main/graph/badge.svg)
   ```

## Status Check Configuration

The pipeline automatically creates status checks that can block merges:

1. **Repository Settings → Branches**
2. **Branch protection rules → main**
3. **Require status checks to pass before merging**
4. **Select:**
   - `contract-tests`
   - `verify-all-contracts`
   - `mutation-testing`

## Slack/Discord Notifications (Optional)

Add to `.github/workflows/contract-verification.yml` at the end of any job:

```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Contract verification failed!'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Environment Variables

Set these in repository settings if needed:

- `COVERAGE_THRESHOLD` - Override default 90%
- `MUTATION_TIMEOUT` - Override default 60 minutes

## Scheduled Runs

Current schedule:
- **Daily verification:** 2:00 AM UTC
- **Nightly certificates:** 3:00 AM UTC

To adjust, edit the cron expression in workflow files:
```yaml
schedule:
  - cron: '0 2 * * *'  # Minute Hour Day Month DayOfWeek
```

## Workflow Dispatch

All workflows support manual triggers:

### Via GitHub UI
1. Actions tab → Select workflow
2. "Run workflow" button → Select branch
3. Click "Run workflow"

### Via GitHub CLI
```bash
gh workflow run contract-verification.yml
gh workflow run nightly-certificate-generation.yml
```

## Artifact Management

Artifacts are automatically cleaned up based on retention policy:

- **Test results:** 30 days
- **Certificates:** 90 days (regular), 365 days (releases)
- **Coverage reports:** 30 days

To download artifacts:
```bash
gh run list --workflow=contract-verification.yml
gh run download <run-id>
```

## Pull Request Integration

Workflows automatically:
- Run on all PRs to main/develop
- Post summary comments
- Block merge if tests fail
- Show coverage diff

## Monitoring & Alerts

### GitHub Actions Email
- Automatically sent on workflow failure
- Configure: Settings → Notifications

### Third-party Monitoring
- https://www.githubstatus.com/ for GitHub Actions status
- Consider https://www.statuscake.com/ for uptime monitoring

## Performance Optimization

If workflows are slow:

1. **Increase parallelization:**
   ```yaml
   strategy:
     matrix:
       test-group: [1, 2, 3]
   ```

2. **Cache dependencies:**
   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
   ```

3. **Use self-hosted runners:**
   - Settings → Actions → Runners → New self-hosted runner

## Troubleshooting

### Workflows not appearing
- Check `.github/workflows/` directory exists
- Verify YAML syntax
- Ensure files end in `.yml` or `.yaml`

### Jobs failing silently
- Check job logs in Actions tab
- Look for "Set up job" and "Complete job" steps
- Verify secrets are set correctly

### Coverage not uploading
- Check `CODECOV_TOKEN` secret
- Verify Codecov repository is enabled
- Review `codecov/codecov-action@v4` step logs

## Best Practices

1. **Always run locally first:**
   ```bash
   ./scripts/validate_pipeline_locally.sh
   ```

2. **Keep workflows DRY:**
   - Use reusable workflows for common tasks
   - Extract repeated steps into composite actions

3. **Monitor resource usage:**
   - Check Actions usage in billing
   - Public repos get unlimited minutes
   - Private repos have limits

4. **Version lock actions:**
   ```yaml
   uses: actions/checkout@v4  # Pin to major version
   ```

5. **Document workflow changes:**
   - Update workflow README
   - Add comments in YAML
   - Note breaking changes

## Security

- Never commit secrets to workflow files
- Use `${{ secrets.SECRET_NAME }}` for sensitive data
- Review third-party actions before use
- Enable Dependabot for action updates:
  ```yaml
  # .github/dependabot.yml
  version: 2
  updates:
    - package-ecosystem: "github-actions"
      directory: "/"
      schedule:
        interval: "weekly"
  ```

## Support

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Workflow Syntax:** https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **Community Forum:** https://github.community/c/code-to-cloud/github-actions/

## Related Files

- Pipeline documentation: `.github/workflows/README.md`
- Setup guide: `CONTRACT_CICD_SETUP.md`
- Quick start: `CONTRACT_CICD_QUICKSTART.md`
