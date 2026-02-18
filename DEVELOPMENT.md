# Development Guide

## 🚀 Quick Start

### Prerequisites

- Python 3.13+ (3.14 works fine)
- MySQL 8.0+ or SQLite (for development)
- Git
- pip and virtualenv

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:MahmoudGh01/M7_KitchenSync_Back.git
   cd M7_KitchenSync_Back
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### Run Specific Tests

```bash
# Single test file
pytest tests/test_auth_service.py

# Single test function
pytest tests/test_auth_service.py::TestAuthService::test_register_user_success

# Tests by marker
pytest -m unit
pytest -m integration
```

### Coverage Requirements

- Minimum: **80%** (enforced in CI)
- Current: **82.55%**

## 🔍 Code Quality

### Run All Linters

```bash
# Using pre-commit (recommended)
pre-commit run --all-files

# Or individually:
ruff check app tests
black app tests --check
isort app tests --check-only
mypy app
bandit -r app
```

### Auto-fix Issues

```bash
# Format code
black app tests
isort app tests

# Fix auto-fixable lint issues
ruff check app tests --fix
```

### Type Checking

```bash
mypy app --ignore-missing-imports
```

## 📦 Dependency Management

We use `pip-tools` for reproducible builds.

### Install pip-tools

```bash
pip install pip-tools
```

### Add New Dependency

1. Add to `requirements.in`
2. Compile lock file:
   ```bash
   pip-compile requirements.in
   ```
3. Install updated dependencies:
   ```bash
   pip-sync requirements.txt
   ```

### Update All Dependencies

```bash
pip-compile requirements.in --upgrade
pip-sync requirements.txt
```

### Update Single Dependency

```bash
pip-compile requirements.in --upgrade-package flask
pip-sync requirements.txt
```

## 🗄️ Database Migrations

We use Alembic for database migrations.

### Create Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1
```

### Check Migration Status

```bash
alembic current
alembic history
```

### Check for Missing Migrations

```bash
alembic check
```

## 🏃 Running the Application

### Development Server

```bash
python wsgi.py
# or
flask run
```

Server runs on `http://localhost:5000`

### Production Server

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Docker

```bash
docker build -t kitchensync-api .
docker run -p 8000:8000 --env-file .env kitchensync-api
```

## 🔧 Pre-commit Hooks

### What Runs on Commit

1. **Trailing whitespace** - Removes trailing spaces
2. **End of file fixer** - Ensures newline at EOF
3. **YAML/JSON validation** - Checks syntax
4. **Large files check** - Prevents >500KB files
5. **Merge conflict check** - Detects conflict markers
6. **Case conflict check** - Prevents case-sensitive issues
7. **Private key detection** - Prevents committing secrets
8. **Black** - Code formatting (100 char line length)
9. **isort** - Import sorting
10. **Ruff** - Fast Python linting
11. **Bandit** - Security vulnerability scanning
12. **mypy** - Static type checking

### Skip Hooks (Emergency Only)

```bash
git commit --no-verify -m "Emergency fix"
```

### Update Hook Versions

```bash
pre-commit autoupdate
```

## 🚀 Deployment

See [README.md - Deployment](README.md#deployment) section.

### Environment Variables

Required for production (see `.env.example`):

- `FLASK_ENV=production`
- `SECRET_KEY` - Flask secret (32+ chars)
- `JWT_SECRET_KEY` - JWT signing key (32+ chars)
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed CORS origins

### Pre-deployment Checklist

- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] Migrations created and tested
- [ ] Environment variables configured
- [ ] Secrets rotated
- [ ] CORS origins restricted
- [ ] DEBUG = False
- [ ] Using gunicorn (not Flask dev server)

## 📊 CI/CD

### Continuous Integration

Every PR triggers:

1. **Linting** (ruff)
2. **Type checking** (mypy)
3. **Tests** (pytest on Python 3.13)
4. **Coverage** (minimum 80%)
5. **Security scan** (bandit, safety)
6. **Migration check** (alembic check)

### Status Badges

- CI: [![CI/CD](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions/workflows/ci.yml/badge.svg)](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions/workflows/ci.yml)
- Coverage: [![codecov](https://codecov.io/gh/MahmoudGh01/M7_KitchenSync_Back/branch/main/graph/badge.svg)](https://codecov.io/gh/MahmoudGh01/M7_KitchenSync_Back)

### Branch Protection

**Main branch** requires:
- All CI checks passing ✅
- At least 1 approval
- No force pushes
- Merge via PR only

## 🐛 Troubleshooting

### Tests Failing Locally

```bash
# Clean test cache
rm -rf .pytest_cache htmlcov .coverage

# Reinstall dependencies
pip install -r requirements.txt

# Run tests verbosely
pytest -vv
```

### Pre-commit Failing

```bash
# Update pre-commit
pre-commit clean
pre-commit install --install-hooks

# Run manually
pre-commit run --all-files
```

### Database Connection Issues

```bash
# Check MySQL is running
mysql -u root -p

# Or use SQLite for development
# In .env: DATABASE_URL=sqlite:///kitchensync.db
```

### Import Errors

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run from project root
cd /path/to/M7_KitchenSync_Back
python wsgi.py
```

## 📚 Additional Resources

- [README.md](README.md) - Project overview and quick start
- [CONFIGURATION.md](CONFIGURATION.md) - Detailed configuration guide
- [API_IMPLEMENTATION.md](API_IMPLEMENTATION.md) - API documentation
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [pytest Docs](https://docs.pytest.org/)
- [Flask Docs](https://flask.palletsprojects.com/)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Make changes and commit: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request
5. Wait for CI checks and review
6. Merge when approved ✅

### Code Style

- Follow PEP 8 (enforced by black/ruff)
- 100 character line length
- snake_case for functions/variables
- Type hints where possible
- Docstrings for public functions

### Commit Messages

```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat: add user authentication endpoint

- Implement JWT token generation
- Add refresh token support
- Include password hashing with passlib

Closes #123
```
