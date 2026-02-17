# M7 KitchenSync API

Flask API with JWT authentication (access + refresh tokens) using Flask-RESTX.

## Requirements

- Python 3.10+ recommended
- pip

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Default configuration is defined in `app/__init__.py`. Update these as needed:

- `SQLALCHEMY_DATABASE_URI` (MySQL)
- `JWT_SECRET_KEY`
- `JWT_ACCESS_TOKEN_EXPIRES` (seconds)
- `JWT_REFRESH_TOKEN_EXPIRES` (seconds)

## Run

```bash
export FLASK_APP=app
flask run --host 0.0.0.0 --port 8000
```

The server starts on `http://0.0.0.0:8000`.

## API Documentation

Swagger UI is available at:

- `http://0.0.0.0:8000/docs`

## Authentication Endpoints

Base path: `/auth`

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

### Register

```bash
curl -X POST http://0.0.0.0:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"display_name":"demo","kitchen_code":"123456","password":"Strong#123"}'
```

### Login

```bash
curl -X POST http://0.0.0.0:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"display_name":"demo","kitchen_code":"123456","password":"Strong#123"}'
```

### Refresh Access Token

```bash
curl -X POST http://0.0.0.0:8000/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

### Get Current User

```bash
curl -X GET http://0.0.0.0:8000/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## Validation Rules

- Kitchen code must be exactly 6 digits.
- Password must be at least 8 characters and include upper, lower, number, and symbol.
