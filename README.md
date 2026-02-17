# KitchenSync API

[![CI/CD](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions/workflows/ci.yml/badge.svg)](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MahmoudGh01/M7_KitchenSync_Back/branch/main/graph/badge.svg)](https://codecov.io/gh/MahmoudGh01/M7_KitchenSync_Back)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Flask-based REST API for managing shared kitchen inventory with JWT authentication, designed for roommates to track items, log consumption, and manage restocking.

## Features

- 🔐 JWT authentication (access + refresh tokens)
- 🏠 Multi-kitchen support with unique 6-digit codes
- 📦 Inventory tracking with percentage-based quantities
- 📊 Automatic status updates (IN_STOCK/NEEDED)
- 📝 Consumption and restock logging
- 📖 Auto-generated Swagger documentation
- 🏥 Health check endpoint with database connectivity monitoring
- 🔄 CORS support for frontend integration
- 📝 Structured logging with rotating file handlers
- 🗄️ Database migrations with Alembic
- ✅ 86% test coverage with 76 passing tests
- 🚀 CI/CD pipeline with automated testing

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo-url>
cd M7_KitchenSync_Back

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Minimum required settings:**
```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/KitchenSyncDB
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-minimum-32-characters
```

📚 **See [CONFIGURATION.md](CONFIGURATION.md) for detailed setup guide**

### 3. Database Setup

**MySQL (Recommended for production):**
```sql
CREATE DATABASE KitchenSyncDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kitchensync'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON KitchenSyncDB.* TO 'kitchensync'@'localhost';
FLUSH PRIVILEGES;
```

**SQLite (Quick development):**
```env
DATABASE_URL=sqlite:///kitchensync.db
```

### 4. Run the Application

**Development mode:**
```bash
python -m app
# Or using Flask CLI
flask run
```

**Production mode:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

The server starts on `http://localhost:5000` (or port specified in `.env`)

### 5. Health Check

Verify the application is running:
```bash
curl http://localhost:5000/health/
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0",
  "timestamp": "2024-02-18T12:00:00Z"
}
```

## API Documentation

Interactive Swagger UI available at:
- **Development:** `http://localhost:5000/docs`
- **Production:** `https://your-domain.com/docs`

## API Overview

### Authentication Endpoints (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get tokens | No |
| POST | `/auth/refresh` | Refresh access token | Refresh token |
| GET | `/auth/me` | Get current user | Access token |

### Kitchen Endpoints (`/kitchens`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/kitchens` | List all kitchens | No |
| POST | `/kitchens` | Create kitchen (auto-generates code) | No |
| GET | `/kitchens/{id}` | Get kitchen by ID | No |
| GET | `/kitchens/code/{code}` | Get kitchen by 6-digit code | No |
| PUT | `/kitchens/{id}` | Update kitchen name | No |
| DELETE | `/kitchens/{id}` | Delete kitchen | No |

### Item Endpoints (`/items`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/items?kitchen_id={id}` | List items by kitchen | Yes |
| POST | `/items` | Create item | Yes |
| GET | `/items/{id}` | Get item details | Yes |
| PUT | `/items/{id}` | Update item | Yes |
| PATCH | `/items/{id}/quantity` | Update quantity only | Yes |
| DELETE | `/items/{id}` | Delete item | Yes |

### Restock Log Endpoints (`/restocks`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/restocks?item_id={id}` | Get restocks by item | Yes |
| GET | `/restocks?kitchen_id={id}` | Get restocks by kitchen | Yes |
| POST | `/restocks` | Log restock (sets item to 100%) | Yes |
| DELETE | `/restocks/{id}` | Delete restock log | Yes |

### Consumption Log Endpoints (`/consumptions`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/consumptions?item_id={id}` | Get consumption by item | Yes |
| GET | `/consumptions?kitchen_id={id}` | Get consumption by kitchen | Yes |
| POST | `/consumptions` | Log consumption (reduces quantity) | Yes |
| DELETE | `/consumptions/{id}` | Delete consumption log | Yes |

## Usage Examples

### Register User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "John",
    "kitchen_code": "123456",
    "password": "Strong#Pass123"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "John",
    "kitchen_code": "123456",
    "password": "Strong#Pass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "user": {
    "id": 1,
    "display_name": "John",
    "kitchen_id": 1
  }
}
```

### Create Item (Authenticated)

```bash
curl -X POST http://localhost:5000/items \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Milk",
    "category": "Dairy",
    "kitchen_id": 1,
    "quantity_percent": 100,
    "low_stock_threshold": 20
  }'
```

### Log Consumption

```bash
curl -X POST http://localhost:5000/consumptions \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "percent_used": 25
  }'
```

📚 **See [API_IMPLEMENTATION.md](API_IMPLEMENTATION.md) for complete API documentation**

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser

# Run specific test file
pytest tests/test_auth_service.py

# Run tests by marker
pytest -m unit
pytest -m integration
```

### Test Coverage

**Current Coverage:** 86% (76 tests passing)

Coverage reports are automatically generated in CI/CD pipeline and uploaded to [Codecov](https://codecov.io/gh/MahmoudGh01/M7_KitchenSync_Back).

### Pre-commit Hooks

We use pre-commit hooks to maintain code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

**Included checks:**
- **Black**: Code formatting (100 char line length)
- **isort**: Import sorting
- **Ruff**: Fast Python linting
- **Bandit**: Security vulnerability scanning
- **mypy**: Static type checking
- File checks (trailing whitespace, EOF, YAML/JSON validation)

### Continuous Integration

Every push and pull request triggers automated:
- Tests on Python 3.14
- Coverage analysis with 80% minimum threshold
- Security scanning (bandit, safety)
- Code quality checks

View CI/CD status: [GitHub Actions](https://github.com/MahmoudGh01/M7_KitchenSync_Back/actions)

## Project Structure

```
M7_KitchenSync_Back/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI/CD pipeline
│       └── main.yml            # Pre-commit hooks
├── app/
│   ├── __init__.py             # Application factory
│   ├── extensions.py           # SQLAlchemy instance
│   ├── models/                 # Database models
│   ├── services/               # Business logic layer
│   ├── controllers/            # Request handling
│   └── routes/                 # API endpoints
├── migrations/                 # Alembic database migrations
├── tests/                      # Test suite (76 tests, 86% coverage)
├── logs/                       # Application logs (rotating)
├── config.py                   # Configuration classes
├── .env.example                # Environment template
├── .env                        # Your secrets (not committed)
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── .coveragerc                 # Coverage configuration
├── pyproject.toml              # Tool configurations
├── pytest.ini                  # Pytest configuration
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Dependencies
├── CONFIGURATION.md            # Setup guide
└── API_IMPLEMENTATION.md       # API documentation
```

## Validation Rules

### Kitchen Code
- Exactly 6 digits
- Unique per kitchen
- Auto-generated on creation

### Password
- Minimum 8 characters
- Must include:
  - Uppercase letter
  - Lowercase letter
  - Number
  - Special character (@$!%*?&#)

### Item Quantity
- 0-100% scale
- Auto-status: 0% = NEEDED, 100% = IN_STOCK
- Clamped to valid range

## Environment Variables

See [CONFIGURATION.md](CONFIGURATION.md) for complete list. Key variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production/testing) | `development` |
| `DATABASE_URL` | Database connection string | MySQL localhost |
| `SECRET_KEY` | Flask secret key | (must set in production) |
| `JWT_SECRET_KEY` | JWT signing key (32+ chars) | (must set in production) |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token lifetime (seconds) | `900` (15 min) |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token lifetime (seconds) | `604800` (7 days) |

## Security Best Practices

- ✅ Never commit `.env` file
- ✅ Use strong random secrets (32+ characters)
- ✅ Change default keys in production
- ✅ Use HTTPS in production
- ✅ Rotate JWT secrets periodically
- ✅ Limit CORS origins to trusted domains
- ✅ Use specific database users (not root)

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app('production')"]
```

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

## Troubleshooting

**Database connection failed:**
```
❌ Database connection failed: Can't connect to MySQL server
```
→ Check `.env` database credentials and ensure MySQL is running

**JWT secret key warning:**
```
ValueError: JWT_SECRET_KEY must be at least 32 characters long!
```
→ Generate a longer secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

**Module not found:**
```
ModuleNotFoundError: No module named 'dotenv'
```
→ Install dependencies: `pip install -r requirements.txt`

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Install pre-commit hooks (`pre-commit install`)
4. Make your changes (hooks will run automatically on commit)
5. Ensure tests pass (`pytest`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open Pull Request

**Code Quality Requirements:**
- All tests must pass (minimum 80% coverage)
- Pre-commit hooks must pass
- Follow PEP 8 naming conventions (snake_case)
- Add tests for new features

## Development Tools

- **Formatting**: Black (100 char line length)
- **Linting**: Ruff (replaces flake8, pylint)
- **Type Checking**: mypy
- **Security**: Bandit
- **Testing**: pytest + pytest-cov
- **Migrations**: Alembic

## License

MIT License - See [LICENSE](LICENSE) file for details

## Support

For issues and questions:
- 📖 Check [CONFIGURATION.md](CONFIGURATION.md)
- 📚 See [API_IMPLEMENTATION.md](API_IMPLEMENTATION.md)
- 🐛 Open an issue on GitHub
