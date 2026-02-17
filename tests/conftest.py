"""
Test configuration and fixtures for pytest.
"""
import pytest
from flask import Flask
from app.extensions import db
from app.Models.UserModel import User
from app.Models.kitchen import Kitchen
from app.Models.item import Item, ItemStatus
from app.Models.restock_log import RestockLog
from app.Models.consumption_log import ConsumptionLog


@pytest.fixture(scope="function")
def app():
    """Create and configure a test Flask app instance."""
    from flask_jwt_extended import JWTManager
    from flask_restx import Api
    from app.Routes.AuthRoutes import auth_ns
    from app.Routes.KitchenRoutes import kitchen_ns
    from app.Routes.ItemRoutes import item_ns
    from app.Routes.RestockLogRoutes import restock_ns
    from app.Routes.ConsumptionLogRoutes import consumption_ns

    test_app = Flask(__name__)
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    test_app.config["JWT_SECRET_KEY"] = "test-secret-key"
    test_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900
    test_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800

    db.init_app(test_app)
    jwt = JWTManager(test_app)
    api = Api(test_app, doc="/docs")
    api.add_namespace(auth_ns)
    api.add_namespace(kitchen_ns)
    api.add_namespace(item_ns)
    api.add_namespace(restock_ns)
    api.add_namespace(consumption_ns)

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Create a database session for tests."""
    with app.app_context():
        yield db.session


@pytest.fixture
def sample_kitchen(db_session):
    """Create a sample kitchen for testing."""
    kitchen = Kitchen(code="123456", name="Test Kitchen")
    db_session.add(kitchen)
    db_session.commit()
    return kitchen


@pytest.fixture
def sample_user(db_session, sample_kitchen):
    """Create a sample user for testing."""
    user = User(display_name="TestUser", kitchen_id=sample_kitchen.id)
    user.set_password("Test#123")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_item(db_session, sample_kitchen):
    """Create a sample item for testing."""
    item = Item(
        name="Test Item",
        category="Test Category",
        kitchen_id=sample_kitchen.id,
        quantity_percent=100.0,
        low_stock_threshold=20.0,
        status=ItemStatus.IN_STOCK,
    )
    db_session.add(item)
    db_session.commit()
    return item


@pytest.fixture
def auth_headers(client, sample_user, sample_kitchen):
    """Get authentication headers with valid JWT token."""
    response = client.post(
        "/auth/login",
        json={
            "display_name": sample_user.display_name,
            "kitchen_code": sample_kitchen.code,
            "password": "Test#123",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
