# Branch Protection & CI/CD Setup Guide

This document describes how to configure branch protection rules and CI/CD for the KitchenSync API repository.

## Branch Protection Rules

### Setting Up Branch Protection

1. Go to **Settings** → **Branches** in your GitHub repository
2. Click **Add rule** under "Branch protection rules"
3. Apply these settings for the `main` (or `master`) branch:

### Required Settings

#### ✅ **Protect matching branches**
- Branch name pattern: `main` (or `master`)

#### ✅ **Require a pull request before merging**
- [x] Require a pull request before merging
- [x] Require approvals: **1**
- [x] Dismiss stale pull request approvals when new commits are pushed
- [ ] Require review from Code Owners (optional)

#### ✅ **Require status checks to pass before merging**
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging

**Required status checks:**
- `Test Python 3.13` (from CI workflow)
- `Security Scan` (from CI workflow)
- `pre-commit.ci - pr` (if using pre-commit.ci)

#### ✅ **Require conversation resolution before merging**
- [x] Require conversation resolution before merging

#### ✅ **Require signed commits** (optional but recommended)
- [x] Require signed commits

#### ✅ **Require linear history** (optional)
- [x] Require linear history
- This enforces rebase/squash merges, no merge commits

#### ✅ **Do not allow bypassing the above settings**
- [x] Do not allow bypassing the above settings
- Applies to administrators too

#### ✅ **Restrict who can push to matching branches**
- [x] Restrict pushes that create matching branches
- Only allow: Administrators, Maintainers (no direct pushes)

### Visual Configuration

```
Branch protection rule for: main

[x] Require a pull request before merging
    Required approvals: 1
    [x] Dismiss stale pull request approvals when new commits are pushed

[x] Require status checks to pass before merging
    [x] Require branches to be up to date before merging
    Status checks that are required:
      - Test Python 3.13
      - Security Scan
      - Build Status

[x] Require conversation resolution before merging
[x] Require linear history
[x] Do not allow bypassing the above settings
[x] Restrict who can push to matching branches
```

## Continuous Integration (CI)

### CI Workflow Checks

The CI pipeline (`.github/workflows/ci.yml`) runs on every:
- Push to `main`/`develop` branches
- Pull request to `main`/`develop` branches

### What CI Validates

1. **Code Quality**
   - ✅ Ruff linting
   - ✅ Black formatting check
   - ✅ isort import sorting

2. **Type Safety**
   - ✅ mypy static type checking

3. **Tests**
   - ✅ All 76 tests must pass
   - ✅ Coverage ≥ 80% required
   - ✅ Tests run on Python 3.13

4. **Security**
   - ✅ Bandit vulnerability scan
   - ✅ Safety dependency check

5. **Database**
   - ✅ Alembic migration validation

### CI Badge

Add to README.md:

```markdown
[![CI/CD](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions/workflows/ci.yml/badge.svg)](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions/workflows/ci.yml)
```

## Continuous Deployment (CD)

### Automatic Deployment Setup

#### Option 1: GitHub Actions (Recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run migrations
        run: |
          alembic upgrade head
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      - name: Deploy to server
        run: |
          # Your deployment commands here
          # Example: Deploy to Heroku, Railway, or custom server
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

#### Option 2: Platform-Specific

**Heroku:**
```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.13.15
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: "kitchensync-api"
    heroku_email: "your-email@example.com"
```

**Railway:**
- Connect GitHub repository
- Enable automatic deployments
- Migrations run via railway.toml:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "alembic upgrade head && gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app"
```

### Required Secrets

Add to **Settings** → **Secrets and variables** → **Actions**:

| Secret | Description |
|--------|-------------|
| `DATABASE_URL` | Production database URL |
| `SECRET_KEY` | Flask secret key |
| `JWT_SECRET_KEY` | JWT secret key |
| `DEPLOY_KEY` | Server SSH key or platform API key |
| `HEROKU_API_KEY` | Heroku API key (if using Heroku) |

### Deployment Environments

Create environments in **Settings** → **Environments**:

1. **production**
   - Require reviewers: Yes (1 required)
   - Wait timer: 0 minutes
   - Environment secrets: Add all production secrets

2. **staging** (optional)
   - No required reviewers
   - Use for testing before production

## Merge Workflow

### Developer Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"
# (pre-commit hooks run automatically)

# 3. Push to GitHub
git push origin feature/new-feature

# 4. Create Pull Request on GitHub

# 5. CI runs automatically:
#    - Linting
#    - Type checking  
#    - Tests
#    - Coverage check
#    - Security scan

# 6. Request review from team member

# 7. Address review comments

# 8. Once approved and CI passes, merge PR

# 9. Automatic deployment to production (if configured)
```

### PR Checklist

Before requesting review:

- [ ] Pre-commit hooks passing locally
- [ ] All tests passing locally (`pytest`)
- [ ] Coverage ≥ 80%
- [ ] No new security vulnerabilities
- [ ] Migrations created (if schema changed)
- [ ] Documentation updated
- [ ] Commit messages follow convention

## Enforcing Quality Gates

### Local Enforcement

```bash
# Pre-commit runs on every commit
git commit -m "Your message"
# Hooks run automatically

# Or run manually
pre-commit run --all-files
```

### CI Enforcement

All PRs must pass:
1. ✅ All pre-commit checks
2. ✅ All tests (76 tests)
3. ✅ Coverage ≥ 80%
4. ✅ Type checking (mypy)
5. ✅ Security scan (bandit)
6. ✅ Migration check (alembic)
7. ✅ At least 1 approval

### Bypassing (Emergency Only)

**DO NOT bypass unless absolutely necessary:**

```bash
# Skip pre-commit (emergency only)
git commit --no-verify -m "Emergency fix"

# Override branch protection (admin only)
# Settings → Branches → Edit rule → Temporarily disable
```

## Monitoring CI/CD

### View CI Status

- Actions tab: https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions
- PR checks: Automatically shown on PR page
- Branch protection: Shows required checks

### Debugging Failed CI

```bash
# View logs in GitHub Actions
# Click on failed job → View logs

# Run locally to reproduce
pytest -v
ruff check app tests
mypy app
bandit -r app
```

## Best Practices

1. **Never commit directly to main**
   - Always use feature branches
   - Create PR for review

2. **Keep PRs small**
   - Easier to review
   - Faster to merge
   - Less risky

3. **Run tests locally before pushing**
   - Saves CI time
   - Faster feedback

4. **Resolve merge conflicts locally**
   - Test after resolving
   - Don't merge with conflicts

5. **Update dependencies regularly**
   - Dependabot creates automated PRs
   - Review and merge weekly

6. **Monitor deployments**
   - Check health endpoint
   - Review logs
   - Set up alerts

## Troubleshooting

### CI Always Failing

```bash
# Pull latest main
git checkout main
git pull origin main

# Rebase your branch
git checkout feature/your-branch
git rebase main

# Fix conflicts
git add .
git rebase --continue

# Force push (after rebase)
git push --force-with-lease
```

### Can't Merge PR

**Reasons:**
- CI checks not passing → Fix issues
- No approval → Request review
- Conflicts → Rebase on main
- Branch not up to date → Update branch

### Deployment Failed

```bash
# Check logs in GitHub Actions
# Rollback if needed
git revert HEAD
git push origin main
```

## Additional Resources

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
