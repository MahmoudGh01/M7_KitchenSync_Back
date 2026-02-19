from __future__ import annotations

from datetime import datetime

from app.extensions import db
from app.models.consumption_log import ConsumptionLog
from app.models.item import Item, ItemStatus


class ConsumptionLogService:
    @staticmethod
    def create_consumption_log(
        user_id: int,
        item_id: int,
        percent_used: float,
    ) -> ConsumptionLog | None:
        """Create a new consumption log and update item quantity."""
        item = Item.query.get(item_id)
        if not item:
            return None

        # Create the consumption log
        log = ConsumptionLog(
            user_id=user_id,
            item_id=item_id,
            percent_used=percent_used,
        )
        db.session.add(log)

        # Update item quantity
        new_quantity = max(0.0, item.quantity_percent - percent_used)
        item.quantity_percent = new_quantity

        # Auto-update status if depleted
        if new_quantity <= 0:
            item.status = ItemStatus.NEEDED

        db.session.commit()
        return log

    @staticmethod
    def get_consumption_log_by_id(log_id: int) -> ConsumptionLog | None:
        """Get a consumption log by ID."""
        return ConsumptionLog.query.get(log_id)

    @staticmethod
    def get_consumption_logs_by_item(item_id: int) -> list[ConsumptionLog]:
        """Get all consumption logs for an item."""
        return ConsumptionLog.query.filter_by(item_id=item_id).order_by(
            ConsumptionLog.created_at.desc()
        ).all()

    @staticmethod
    def get_consumption_logs_by_kitchen(kitchen_id: int) -> list[ConsumptionLog]:
        """Get all consumption logs for a kitchen."""
        return (
            ConsumptionLog.query.join(Item)
            .filter(Item.kitchen_id == kitchen_id)
            .order_by(ConsumptionLog.created_at.desc())
            .all()
        )

    @staticmethod
    def get_consumption_logs_by_user(user_id: int) -> list[ConsumptionLog]:
        """Get all consumption logs for a user."""
        return ConsumptionLog.query.filter_by(user_id=user_id).order_by(
            ConsumptionLog.created_at.desc()
        ).all()

    @staticmethod
    def delete_consumption_log(log_id: int) -> bool:
        """Delete a consumption log."""
        log = ConsumptionLog.query.get(log_id)
        if not log:
            return False
        db.session.delete(log)
        db.session.commit()
        return True
