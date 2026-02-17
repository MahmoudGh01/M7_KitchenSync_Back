"""
Unit tests for KitchenService.
"""
import pytest
from app.services.kitchen_service import KitchenService
from app.models.kitchen import Kitchen


@pytest.mark.unit
@pytest.mark.service
class TestKitchenService:
    """Test KitchenService methods."""

    def test_generate_unique_code(self, app):
        """Test unique kitchen code generation."""
        with app.app_context():
            code = KitchenService.generate_unique_code()
            assert isinstance(code, str)
            assert len(code) == 6
            assert code.isdigit()

    def test_create_kitchen(self, app):
        """Test kitchen creation."""
        with app.app_context():
            kitchen = KitchenService.create_kitchen(name="New Kitchen")
            assert kitchen is not None
            assert kitchen.name == "New Kitchen"
            assert len(kitchen.code) == 6
            assert kitchen.code.isdigit()

    def test_get_kitchen_by_id(self, app, sample_kitchen):
        """Test getting kitchen by ID."""
        with app.app_context():
            kitchen = KitchenService.get_kitchen_by_id(sample_kitchen.id)
            assert kitchen is not None
            assert kitchen.id == sample_kitchen.id
            assert kitchen.name == sample_kitchen.name

    def test_get_kitchen_by_id_not_found(self, app):
        """Test getting non-existent kitchen by ID."""
        with app.app_context():
            kitchen = KitchenService.get_kitchen_by_id(99999)
            assert kitchen is None

    def test_get_kitchen_by_code(self, app, sample_kitchen):
        """Test getting kitchen by code."""
        with app.app_context():
            kitchen = KitchenService.get_kitchen_by_code(sample_kitchen.code)
            assert kitchen is not None
            assert kitchen.code == sample_kitchen.code

    def test_get_kitchen_by_code_not_found(self, app):
        """Test getting non-existent kitchen by code."""
        with app.app_context():
            kitchen = KitchenService.get_kitchen_by_code("999999")
            assert kitchen is None

    def test_get_all_kitchens(self, app, sample_kitchen):
        """Test getting all kitchens."""
        with app.app_context():
            kitchens = KitchenService.get_all_kitchens()
            assert len(kitchens) >= 1
            assert any(k.id == sample_kitchen.id for k in kitchens)

    def test_update_kitchen(self, app, sample_kitchen):
        """Test updating kitchen name."""
        with app.app_context():
            updated = KitchenService.update_kitchen(
                sample_kitchen.id, "Updated Kitchen"
            )
            assert updated is not None
            assert updated.name == "Updated Kitchen"
            assert updated.id == sample_kitchen.id

    def test_update_kitchen_not_found(self, app):
        """Test updating non-existent kitchen."""
        with app.app_context():
            updated = KitchenService.update_kitchen(99999, "New Name")
            assert updated is None

    def test_delete_kitchen(self, app, sample_kitchen):
        """Test deleting kitchen."""
        with app.app_context():
            success = KitchenService.delete_kitchen(sample_kitchen.id)
            assert success is True
            kitchen = KitchenService.get_kitchen_by_id(sample_kitchen.id)
            assert kitchen is None

    def test_delete_kitchen_not_found(self, app):
        """Test deleting non-existent kitchen."""
        with app.app_context():
            success = KitchenService.delete_kitchen(99999)
            assert success is False
