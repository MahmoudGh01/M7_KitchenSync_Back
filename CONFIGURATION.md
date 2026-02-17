# Configuration Guide

## Environment Setup

KitchenSync API uses environment variables for configuration. This guide explains how to set up your environment for different deployment scenarios.

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python -m app
   ```

## Environment Variables

### Required Settings

#### Database Configuration

Choose ONE of the following approaches:

**Option 1: Use DATABASE_URL (Recommended)**
```env
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/KitchenSyncDB
```

**Option 2: Use Individual Components**
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=KitchenSyncDB
DB_USER=root
DB_PASSWORD=your_password_here
```

#### Security Settings

**CRITICAL: Change these in production!**

```env
SECRET_KEY=your-secret-key-minimum-32-characters-long-random-string
JWT_SECRET_KEY=your-jwt-secret-minimum-32-characters-long-random-string
```

Generate secure random keys:
```bash
# Generate a secure random key (Linux/Mac)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use this online: https://1password.com/password-generator/
```

### Optional Settings

#### Flask Configuration
```env
FLASK_ENV=development          # Options: development, production, testing
FLASK_DEBUG=True              # Enable debug mode
PORT=5000                     # Server port
```

#### JWT Token Expiration
```env
JWT_ACCESS_TOKEN_EXPIRES=900      # 15 minutes (in seconds)
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days (in seconds)
```

#### API Documentation
```env
API_TITLE=KitchenSync API
API_VERSION=1.0
API_DESCRIPTION=Kitchen inventory management API
```

#### CORS (Cross-Origin Resource Sharing)
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### Logging
```env
LOG_LEVEL=INFO                # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/kitchensync.log
```

## Configuration Environments

### Development Environment

**File: `.env`**
```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/KitchenSyncDB
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret-key-minimum-32-characters
```

Features:
- Debug mode enabled
- SQL queries logged to console
- Auto-reload on code changes
- Less strict validation

### Production Environment

**File: `.env`**
```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=mysql+mysqlconnector://user:strong_password@db.example.com:3306/kitchensync_prod
SECRET_KEY=<generate-secure-random-key>
JWT_SECRET_KEY=<generate-secure-random-key-minimum-32-characters>
LOG_LEVEL=WARNING
```

Features:
- Debug mode disabled
- Strict secret key validation
- Production-optimized settings
- Error logging only

**Production Checklist:**
- ✅ Change SECRET_KEY from default
- ✅ Change JWT_SECRET_KEY from default (minimum 32 chars)
- ✅ Use strong database password
- ✅ Set FLASK_DEBUG=False
- ✅ Use environment-specific database
- ✅ Configure proper CORS_ORIGINS
- ✅ Set up proper logging

### Testing Environment

Tests automatically use the testing configuration with SQLite in-memory database. No `.env` file needed for testing.

```bash
pytest
```

## Database Setup

### MySQL (Production/Development)

1. **Install MySQL:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install mysql-server

   # macOS
   brew install mysql
   ```

2. **Create Database:**
   ```sql
   mysql -u root -p
   CREATE DATABASE KitchenSyncDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'kitchensync'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON KitchenSyncDB.* TO 'kitchensync'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Update .env:**
   ```env
   DATABASE_URL=mysql+mysqlconnector://kitchensync:your_password@localhost:3306/KitchenSyncDB
   ```

### SQLite (Development/Testing)

For lightweight development:

```env
DATABASE_URL=sqlite:///kitchensync.db
```

## Running the Application

### Development Mode
```bash
# Using Flask CLI
flask run

# Or using Python
python -m app

# With custom port
FLASK_RUN_PORT=8000 flask run
```

### Production Mode

**Using Gunicorn (Recommended):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

**Using uWSGI:**
```bash
pip install uwsgi
uwsgi --http :8000 --wsgi-file app/__init__.py --callable app
```

## Troubleshooting

### Common Issues

**1. Database Connection Failed**
```
❌ Database connection failed: Can't connect to MySQL server
```
**Solution:** Check database credentials in `.env` and ensure MySQL is running

**2. Invalid JWT Secret Key**
```
ValueError: JWT_SECRET_KEY must be at least 32 characters long!
```
**Solution:** Generate a longer secret key (see Security Settings above)

**3. Module Not Found**
```
ModuleNotFoundError: No module named 'dotenv'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

**4. Port Already in Use**
```
OSError: [Errno 48] Address already in use
```
**Solution:** Use a different port: `FLASK_RUN_PORT=8000 flask run`

## Environment File Location

The application looks for `.env` in the project root directory:
```
M7_KitchenSync_Back/
├── .env                  # Your environment variables (DO NOT COMMIT)
├── .env.example          # Example template (safe to commit)
├── config.py            # Configuration classes
├── app/
│   └── __init__.py      # Application factory
└── requirements.txt
```

**IMPORTANT:** Never commit `.env` to version control! It's already in `.gitignore`.

## Security Best Practices

1. **Never commit secrets** - Use `.env` for local, environment variables for production
2. **Rotate keys regularly** - Change SECRET_KEY and JWT_SECRET_KEY periodically
3. **Use strong passwords** - Minimum 32 characters for secrets
4. **Restrict database access** - Use specific database users, not root
5. **Enable HTTPS** - Always use SSL/TLS in production
6. **Limit CORS origins** - Only allow trusted domains
7. **Review logs** - Monitor for suspicious activity

## Docker Configuration

If using Docker, pass environment variables:

```dockerfile
# Dockerfile
ENV FLASK_ENV=production
ENV DATABASE_URL=mysql+mysqlconnector://user:pass@db:3306/kitchensync
```

Or use docker-compose:

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    env_file: .env
    environment:
      - FLASK_ENV=production
    ports:
      - "5000:5000"
```

## Further Reading

- [Flask Configuration](https://flask.palletsprojects.com/en/3.0.x/config/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
