"""
Unit tests for AuthService.
"""
import pytest
from app.services.auth_service import AuthService
from app.models.user_model import User
from app.models.kitchen import Kitchen


@pytest.mark.unit
@pytest.mark.service
class TestAuthService:
    """Test AuthService methods."""

    def test_register_user_success(self, app, sample_kitchen):
        """Test successful user registration."""
        with app.app_context():
            user = AuthService.register_user(
                display_name="NewUser",
                password="Strong#123",
                kitchen_code=sample_kitchen.code,
            )
            assert user is not None
            assert user.display_name == "NewUser"
            assert user.kitchen_id == sample_kitchen.id
            assert user.is_active is True

    def test_register_user_invalid_kitchen(self, app):
        """Test registration with invalid kitchen code."""
        with app.app_context():
            with pytest.raises(ValueError, match="Kitchen not found"):
                AuthService.register_user(
                    display_name="NewUser",
                    password="Strong#123",
                    kitchen_code="999999",
                )

    def test_register_user_duplicate(self, app, sample_user, sample_kitchen):
        """Test registration with duplicate display name in same kitchen."""
        with app.app_context():
            with pytest.raises(ValueError, match="Display name already in use"):
                AuthService.register_user(
                    display_name=sample_user.display_name,
                    password="Strong#123",
                    kitchen_code=sample_kitchen.code,
                )

    def test_authenticate_user_success(self, app, sample_user, sample_kitchen):
        """Test successful user authentication."""
        with app.app_context():
            user = AuthService.authenticate_user(
                display_name=sample_user.display_name,
                password="Test#123",
                kitchen_code=sample_kitchen.code,
            )
            assert user is not None
            assert user.id == sample_user.id

    def test_authenticate_user_wrong_password(self, app, sample_user, sample_kitchen):
        """Test authentication with wrong password."""
        with app.app_context():
            user = AuthService.authenticate_user(
                display_name=sample_user.display_name,
                password="WrongPassword",
                kitchen_code=sample_kitchen.code,
            )
            assert user is None

    def test_authenticate_user_invalid_kitchen(self, app, sample_user):
        """Test authentication with invalid kitchen code."""
        with app.app_context():
            user = AuthService.authenticate_user(
                display_name=sample_user.display_name,
                password="Test#123",
                kitchen_code="999999",
            )
            assert user is None

    def test_authenticate_user_not_exists(self, app, sample_kitchen):
        """Test authentication with non-existent user."""
        with app.app_context():
            user = AuthService.authenticate_user(
                display_name="NonExistent",
                password="Test#123",
                kitchen_code=sample_kitchen.code,
            )
            assert user is None

    def test_authenticate_inactive_user(self, app, sample_user, sample_kitchen, db_session):
        """Test authentication with inactive user."""
        with app.app_context():
            sample_user.is_active = False
            db_session.commit()

            user = AuthService.authenticate_user(
                display_name=sample_user.display_name,
                password="Test#123",
                kitchen_code=sample_kitchen.code,
            )
            assert user is None

    def test_generate_tokens(self, app, sample_user):
        """Test JWT token generation."""
        with app.app_context():
            tokens = AuthService.generate_tokens(sample_user)
            assert "access_token" in tokens
            assert "refresh_token" in tokens
            assert isinstance(tokens["access_token"], str)
            assert isinstance(tokens["refresh_token"], str)

    def test_refresh_access_token(self, app, sample_user):
        """Test access token refresh."""
        with app.app_context():
            new_token = AuthService.refresh_access_token(sample_user.id)
            assert isinstance(new_token, str)
            assert len(new_token) > 0
