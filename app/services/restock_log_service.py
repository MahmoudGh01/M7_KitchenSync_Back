from __future__ import annotations

from typing import Optional
from datetime import datetime

from app.extensions import db
from app.models.restock_log import RestockLog
from app.models.item import Item, ItemStatus


class RestockLogService:
    @staticmethod
    def create_restock_log(user_id: int, item_id: int) -> Optional[RestockLog]:
        """Create a new restock log and update item to full stock."""
        item = Item.query.get(item_id)
        if not item:
            return None

        # Create the restock log
        log = RestockLog(user_id=user_id, item_id=item_id)
        db.session.add(log)

        # Update item to full stock
        item.quantity_percent = 100.0
        item.status = ItemStatus.IN_STOCK

        db.session.commit()
        return log

    @staticmethod
    def get_restock_log_by_id(log_id: int) -> Optional[RestockLog]:
        """Get a restock log by ID."""
        return RestockLog.query.get(log_id)

    @staticmethod
    def get_restock_logs_by_item(item_id: int) -> list[RestockLog]:
        """Get all restock logs for an item."""
        return RestockLog.query.filter_by(item_id=item_id).order_by(
            RestockLog.created_at.desc()
        ).all()

    @staticmethod
    def get_restock_logs_by_kitchen(kitchen_id: int) -> list[RestockLog]:
        """Get all restock logs for a kitchen."""
        return (
            RestockLog.query.join(Item)
            .filter(Item.kitchen_id == kitchen_id)
            .order_by(RestockLog.created_at.desc())
            .all()
        )

    @staticmethod
    def get_restock_logs_by_user(user_id: int) -> list[RestockLog]:
        """Get all restock logs for a user."""
        return RestockLog.query.filter_by(user_id=user_id).order_by(
            RestockLog.created_at.desc()
        ).all()

    @staticmethod
    def delete_restock_log(log_id: int) -> bool:
        """Delete a restock log."""
        log = RestockLog.query.get(log_id)
        if not log:
            return False
        db.session.delete(log)
        db.session.commit()
        return True
