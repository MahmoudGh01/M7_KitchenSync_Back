"""
Unit tests for ItemService.
"""
import pytest
from app.Services.ItemService import ItemService
from app.Models.item import Item, ItemStatus


@pytest.mark.unit
@pytest.mark.service
class TestItemService:
    """Test ItemService methods."""

    def test_create_item(self, app, sample_kitchen):
        """Test item creation."""
        with app.app_context():
            item = ItemService.create_item(
                name="New Item",
                kitchen_id=sample_kitchen.id,
                category="Food",
                quantity_percent=50.0,
                low_stock_threshold=15.0,
                status=ItemStatus.IN_STOCK,
            )
            assert item is not None
            assert item.name == "New Item"
            assert item.kitchen_id == sample_kitchen.id
            assert item.category == "Food"
            assert item.quantity_percent == 50.0
            assert item.low_stock_threshold == 15.0
            assert item.status == ItemStatus.IN_STOCK

    def test_create_item_defaults(self, app, sample_kitchen):
        """Test item creation with default values."""
        with app.app_context():
            item = ItemService.create_item(
                name="Default Item",
                kitchen_id=sample_kitchen.id,
            )
            assert item.quantity_percent == 100.0
            assert item.low_stock_threshold == 20.0
            assert item.status == ItemStatus.IN_STOCK
            assert item.category is None

    def test_get_item_by_id(self, app, sample_item):
        """Test getting item by ID."""
        with app.app_context():
            item = ItemService.get_item_by_id(sample_item.id)
            assert item is not None
            assert item.id == sample_item.id
            assert item.name == sample_item.name

    def test_get_item_by_id_not_found(self, app):
        """Test getting non-existent item."""
        with app.app_context():
            item = ItemService.get_item_by_id(99999)
            assert item is None

    def test_get_items_by_kitchen(self, app, sample_kitchen, sample_item):
        """Test getting all items for a kitchen."""
        with app.app_context():
            items = ItemService.get_items_by_kitchen(sample_kitchen.id)
            assert len(items) >= 1
            assert any(i.id == sample_item.id for i in items)

    def test_update_item(self, app, sample_item):
        """Test updating item."""
        with app.app_context():
            updated = ItemService.update_item(
                sample_item.id,
                name="Updated Item",
                category="New Category",
                quantity_percent=75.0,
                low_stock_threshold=25.0,
                status=ItemStatus.NEEDED,
            )
            assert updated is not None
            assert updated.name == "Updated Item"
            assert updated.category == "New Category"
            assert updated.quantity_percent == 75.0
            assert updated.low_stock_threshold == 25.0
            assert updated.status == ItemStatus.NEEDED

    def test_update_item_partial(self, app, sample_item):
        """Test partial item update."""
        with app.app_context():
            original_category = sample_item.category
            updated = ItemService.update_item(
                sample_item.id,
                name="New Name Only",
            )
            assert updated.name == "New Name Only"
            assert updated.category == original_category

    def test_update_item_not_found(self, app):
        """Test updating non-existent item."""
        with app.app_context():
            updated = ItemService.update_item(99999, name="Test")
            assert updated is None

    def test_delete_item(self, app, sample_item):
        """Test deleting item."""
        with app.app_context():
            success = ItemService.delete_item(sample_item.id)
            assert success is True
            item = ItemService.get_item_by_id(sample_item.id)
            assert item is None

    def test_delete_item_not_found(self, app):
        """Test deleting non-existent item."""
        with app.app_context():
            success = ItemService.delete_item(99999)
            assert success is False

    def test_update_quantity(self, app, sample_item):
        """Test updating item quantity."""
        with app.app_context():
            updated = ItemService.update_quantity(sample_item.id, 50.0)
            assert updated is not None
            assert updated.quantity_percent == 50.0

    def test_update_quantity_clamps_min(self, app, sample_item):
        """Test quantity clamping to minimum."""
        with app.app_context():
            updated = ItemService.update_quantity(sample_item.id, -10.0)
            assert updated.quantity_percent == 0.0

    def test_update_quantity_clamps_max(self, app, sample_item):
        """Test quantity clamping to maximum."""
        with app.app_context():
            updated = ItemService.update_quantity(sample_item.id, 150.0)
            assert updated.quantity_percent == 100.0

    def test_update_quantity_auto_status_needed(self, app, sample_item):
        """Test auto-status update when quantity is 0."""
        with app.app_context():
            updated = ItemService.update_quantity(sample_item.id, 0.0)
            assert updated.status == ItemStatus.NEEDED

    def test_update_quantity_auto_status_in_stock(self, app, sample_item):
        """Test auto-status update when quantity is 100."""
        with app.app_context():
            sample_item.status = ItemStatus.NEEDED
            updated = ItemService.update_quantity(sample_item.id, 100.0)
            assert updated.status == ItemStatus.IN_STOCK

    def test_update_quantity_not_found(self, app):
        """Test updating quantity for non-existent item."""
        with app.app_context():
            updated = ItemService.update_quantity(99999, 50.0)
            assert updated is None
