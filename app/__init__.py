"""
KitchenSync API Application Factory.
"""
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from dotenv import load_dotenv

# Load environment variables BEFORE importing config
load_dotenv()

from config import get_config
from app.extensions import db, cors
from app.models.user_model import User
from app.models.kitchen import Kitchen
from app.models.item import Item
from app.models.restock_log import RestockLog
from app.models.consumption_log import ConsumptionLog
from app.routes.auth_routes import auth_ns
from app.routes.kitchen_routes import kitchen_ns
from app.routes.item_routes import item_ns
from app.routes.restock_log_routes import restock_ns
from app.routes.consumption_log_routes import consumption_ns
from app.controllers.health_controller import health_ns


def create_app(config_name: str = None) -> Flask:
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration environment (development/production/testing)
                    If None, uses FLASK_ENV environment variable
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Validate production config
    if config_name == 'production':
        config_class.validate()
    
    # Setup logging
    config_class.setup_logging(app)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Initialize CORS with configuration
    cors.init_app(
        app,
        origins=app.config.get('CORS_ORIGINS', ['*']),
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
    )
    
    # Initialize API documentation
    api = Api(
        app,
        doc="/docs",
        title=app.config['API_TITLE'],
        version=app.config['API_VERSION'],
        description=app.config['API_DESCRIPTION']
    )
    
    # Register API namespaces
    api.add_namespace(health_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(kitchen_ns)
    api.add_namespace(item_ns)
    api.add_namespace(restock_ns)
    api.add_namespace(consumption_ns)
    
    # Create database tables
    with app.app_context():
        try:
            db.engine.connect()
            app.logger.info("Database connected successfully")
            app.logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else app.config['SQLALCHEMY_DATABASE_URI']}")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
        
        db.create_all()
        app.logger.info("Database tables created/verified")
    
    return app


# Create default app instance for development
app = create_app()

if __name__ == "__main__":
    # Run the development server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
