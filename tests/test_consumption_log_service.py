"""
Unit tests for ConsumptionLogService.
"""
import pytest
from app.services.consumption_log_service import ConsumptionLogService
from app.models.item import ItemStatus


@pytest.mark.unit
@pytest.mark.service
class TestConsumptionLogService:
    """Test ConsumptionLogService methods."""

    def test_create_consumption_log(self, app, db_session, sample_user, sample_item):
        """Test creating a consumption log."""
        with app.app_context():
            sample_item.quantity_percent = 100.0
            db_session.commit()  # Commit the change before service call
            item_id = sample_item.id  # Save ID before detachment
            
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=item_id,
                percent_used=25.0,
            )
            assert log is not None
            assert log.user_id == sample_user.id
            assert log.item_id == item_id
            assert log.percent_used == 25.0
            
            # Query item again to see changes
            from app.models.item import Item
            updated_item = Item.query.get(item_id)
            # Check that item quantity was reduced
            assert updated_item.quantity_percent == 75.0

    def test_create_consumption_log_depletes_item(self, app, db_session, sample_user, sample_item):
        """Test consumption log that depletes item."""
        with app.app_context():
            sample_item.quantity_percent = 30.0
            db_session.commit()  # Commit the change before service call
            item_id = sample_item.id  # Save ID before detachment
            
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=item_id,
                percent_used=40.0,
            )
            assert log is not None
            
            # Query item again to see changes
            from app.models.item import Item
            updated_item = Item.query.get(item_id)
            # Check that item is depleted and status updated
            assert updated_item.quantity_percent == 0.0
            assert updated_item.status == ItemStatus.NEEDED

    def test_create_consumption_log_invalid_item(self, app, sample_user):
        """Test creating consumption log with invalid item."""
        with app.app_context():
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=99999,
                percent_used=25.0,
            )
            assert log is None

    def test_get_consumption_log_by_id(self, app, sample_user, sample_item):
        """Test getting consumption log by ID."""
        with app.app_context():
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
                percent_used=10.0,
            )
            retrieved = ConsumptionLogService.get_consumption_log_by_id(log.id)
            assert retrieved is not None
            assert retrieved.id == log.id

    def test_get_consumption_log_by_id_not_found(self, app):
        """Test getting non-existent consumption log."""
        with app.app_context():
            log = ConsumptionLogService.get_consumption_log_by_id(99999)
            assert log is None

    def test_get_consumption_logs_by_item(self, app, sample_user, sample_item):
        """Test getting consumption logs by item."""
        with app.app_context():
            log1 = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
                percent_used=10.0,
            )
            log2 = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
                percent_used=15.0,
            )
            
            logs = ConsumptionLogService.get_consumption_logs_by_item(sample_item.id)
            assert len(logs) >= 2
            log_ids = [log_entry.id for log_entry in logs]
            assert log1.id in log_ids
            assert log2.id in log_ids

    def test_get_consumption_logs_by_kitchen(self, app, sample_user, sample_item, sample_kitchen):
        """Test getting consumption logs by kitchen."""
        with app.app_context():
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
                percent_used=20.0,
            )
            
            logs = ConsumptionLogService.get_consumption_logs_by_kitchen(sample_kitchen.id)
            assert len(logs) >= 1
            assert any(log_entry.id == log.id for log_entry in logs)

    def test_get_consumption_logs_by_user(self, app, sample_user, sample_item):
        """Test getting consumption logs by user."""
        with app.app_context():
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
                percent_used=30.0,
            )
            
            logs = ConsumptionLogService.get_consumption_logs_by_user(sample_user.id)
            assert len(logs) >= 1
            assert any(log_entry.id == log.id for log_entry in logs)

    def test_delete_consumption_log(self, app, sample_user, sample_item):
        """Test deleting a consumption log."""
        with app.app_context():
            log = ConsumptionLogService.create_consumption_log(
                user_id=sample_user.id,
                item_id=sample_item.id,
                percent_used=5.0,
            )
            
            success = ConsumptionLogService.delete_consumption_log(log.id)
            assert success is True
            
            retrieved = ConsumptionLogService.get_consumption_log_by_id(log.id)
            assert retrieved is None

    def test_delete_consumption_log_not_found(self, app):
        """Test deleting non-existent consumption log."""
        with app.app_context():
            success = ConsumptionLogService.delete_consumption_log(99999)
            assert success is False
