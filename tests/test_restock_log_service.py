"""
Unit tests for RestockLogService.
"""
import pytest
from app.services.restock_log_service import RestockLogService
from app.models.item import ItemStatus


@pytest.mark.unit
@pytest.mark.service
class TestRestockLogService:
    """Test RestockLogService methods."""

    def test_create_restock_log(self, app, db_session, sample_user, sample_item):
        """Test creating a restock log."""
        with app.app_context():
            # Set item to low quantity first
            sample_item.quantity_percent = 30.0
            sample_item.status = ItemStatus.NEEDED
            db_session.commit()  # Commit the change before service call
            item_id = sample_item.id  # Save ID before detachment

            log = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=item_id,
            )
            assert log is not None
            assert log.user_id == sample_user.id
            assert log.item_id == item_id
            
            # Query item again to see changes
            from app.models.item import Item
            updated_item = Item.query.get(item_id)
            # Check that item was restocked
            assert updated_item.quantity_percent == 100.0
            assert updated_item.status == ItemStatus.IN_STOCK

    def test_create_restock_log_invalid_item(self, app, sample_user):
        """Test creating restock log with invalid item."""
        with app.app_context():
            log = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=99999,
            )
            assert log is None

    def test_get_restock_log_by_id(self, app, sample_user, sample_item):
        """Test getting restock log by ID."""
        with app.app_context():
            log = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
            )
            retrieved = RestockLogService.get_restock_log_by_id(log.id)
            assert retrieved is not None
            assert retrieved.id == log.id

    def test_get_restock_log_by_id_not_found(self, app):
        """Test getting non-existent restock log."""
        with app.app_context():
            log = RestockLogService.get_restock_log_by_id(99999)
            assert log is None

    def test_get_restock_logs_by_item(self, app, sample_user, sample_item):
        """Test getting restock logs by item."""
        with app.app_context():
            log1 = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
            )
            log2 = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
            )
            
            logs = RestockLogService.get_restock_logs_by_item(sample_item.id)
            assert len(logs) >= 2
            log_ids = [log_entry.id for log_entry in logs]
            assert log1.id in log_ids
            assert log2.id in log_ids

    def test_get_restock_logs_by_kitchen(self, app, sample_user, sample_item, sample_kitchen):
        """Test getting restock logs by kitchen."""
        with app.app_context():
            log = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
            )
            
            logs = RestockLogService.get_restock_logs_by_kitchen(sample_kitchen.id)
            assert len(logs) >= 1
            assert any(log_entry.id == log.id for log_entry in logs)

    def test_get_restock_logs_by_user(self, app, sample_user, sample_item):
        """Test getting restock logs by user."""
        with app.app_context():
            log = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
            )
            
            logs = RestockLogService.get_restock_logs_by_user(sample_user.id)
            assert len(logs) >= 1
            assert any(log_entry.id == log.id for log_entry in logs)

    def test_delete_restock_log(self, app, sample_user, sample_item):
        """Test deleting a restock log."""
        with app.app_context():
            log = RestockLogService.create_restock_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
            )
            
            success = RestockLogService.delete_restock_log(log.id)
            assert success is True
            
            retrieved = RestockLogService.get_restock_log_by_id(log.id)
            assert retrieved is None

    def test_delete_restock_log_not_found(self, app):
        """Test deleting non-existent restock log."""
        with app.app_context():
            success = RestockLogService.delete_restock_log(99999)
            assert success is False
