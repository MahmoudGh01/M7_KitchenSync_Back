from __future__ import annotations

from typing import Optional

from app.extensions import db
from app.models.item import Item, ItemStatus


class ItemService:
    @staticmethod
    def create_item(
        name: str,
        kitchen_id: int,
        category: Optional[str] = None,
        quantity_percent: float = 100.0,
        low_stock_threshold: float = 20.0,
        status: ItemStatus = ItemStatus.IN_STOCK,
    ) -> Item:
        """Create a new item."""
        item = Item(
            name=name,
            kitchen_id=kitchen_id,
            category=category,
            quantity_percent=quantity_percent,
            low_stock_threshold=low_stock_threshold,
            status=status,
        )
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_item_by_id(item_id: int) -> Optional[Item]:
        """Get an item by ID."""
        return Item.query.get(item_id)

    @staticmethod
    def get_items_by_kitchen(kitchen_id: int) -> list[Item]:
        """Get all items for a kitchen."""
        return Item.query.filter_by(kitchen_id=kitchen_id).all()

    @staticmethod
    def update_item(
        item_id: int,
        name: Optional[str] = None,
        category: Optional[str] = None,
        quantity_percent: Optional[float] = None,
        low_stock_threshold: Optional[float] = None,
        status: Optional[ItemStatus] = None,
    ) -> Optional[Item]:
        """Update an item."""
        item = Item.query.get(item_id)
        if not item:
            return None

        if name is not None:
            item.name = name
        if category is not None:
            item.category = category
        if quantity_percent is not None:
            item.quantity_percent = quantity_percent
        if low_stock_threshold is not None:
            item.low_stock_threshold = low_stock_threshold
        if status is not None:
            item.status = status

        db.session.commit()
        return item

    @staticmethod
    def delete_item(item_id: int) -> bool:
        """Delete an item."""
        item = Item.query.get(item_id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    @staticmethod
    def update_quantity(item_id: int, quantity_percent: float) -> Optional[Item]:
        """Update item quantity and adjust status if needed."""
        item = Item.query.get(item_id)
        if not item:
            return None

        item.quantity_percent = max(0.0, min(100.0, quantity_percent))

        # Auto-update status based on quantity
        if item.quantity_percent <= 0:
            item.status = ItemStatus.NEEDED
        elif item.quantity_percent >= 100:
            item.status = ItemStatus.IN_STOCK

        db.session.commit()
        return item
