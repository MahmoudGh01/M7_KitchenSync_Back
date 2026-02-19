"""
Configuration module for KitchenSync API.
Loads configuration from environment variables with sensible defaults.
"""

from __future__ import annotations

import logging
import os
from datetime import timedelta


class Config:
    """Base configuration class with common settings."""

    # Flask Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")  # nosec

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Database Configuration
    # Support both DATABASE_URL and individual components
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "3306")
        DB_NAME = os.getenv("DB_NAME", "KitchenSyncDB")
        DB_USER = os.getenv("DB_USER", "root")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DATABASE_URL = (
            f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "dev-jwt-secret-key-minimum-32-characters"
    )  # nosec
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "900")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "604800"))
    )

    # API Documentation Configuration
    API_TITLE = os.getenv("API_TITLE", "KitchenSync API")
    API_VERSION = os.getenv("API_VERSION", "1.0")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION", "Kitchen inventory management API")

    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/kitchensync.log")

    @staticmethod
    def setup_logging(app):
        """Configure logging for the application."""
        import os
        from logging.handlers import RotatingFileHandler

        # Get log level from config
        log_level_str = app.config.get("LOG_LEVEL", "INFO")
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)

        # Set Flask app logger level
        app.logger.setLevel(log_level)

        # Remove existing handlers
        app.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        app.logger.addHandler(console_handler)

        # File handler (if LOG_FILE is configured)
        log_file = app.config.get("LOG_FILE")
        if log_file:
            # Create logs directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=10)  # 10MB
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            app.logger.addHandler(file_handler)

        # Log startup message
        app.logger.info(f"KitchenSync API started - Logging level: {log_level_str}")


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    FLASK_ENV = "development"
    SQLALCHEMY_ECHO = True  # Log SQL queries in development


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    FLASK_ENV = "production"

    # Ensure critical settings are provided in production
    @classmethod
    def validate(cls):
        """Validate that required production settings are configured."""
        if cls.SECRET_KEY == "dev-secret-key-change-in-production":  # nosec
            raise ValueError("SECRET_KEY must be set in production!")
        if cls.JWT_SECRET_KEY == "dev-jwt-secret-key-minimum-32-characters":  # nosec
            raise ValueError("JWT_SECRET_KEY must be set in production!")
        if len(cls.JWT_SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long!")


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret-key"  # nosec
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(env: str = None) -> type[Config]:
    """
    Get configuration class based on environment.

    Args:
        env: Environment name (development/production/testing)
             If None, uses FLASK_ENV environment variable

    Returns:
        Configuration class for the specified environment
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development")

    return config.get(env, config["default"])
