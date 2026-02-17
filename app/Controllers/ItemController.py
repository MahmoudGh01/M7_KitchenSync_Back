from __future__ import annotations

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.Services.ItemService import ItemService
from app.Models.item import ItemStatus


def _get_json() -> dict:
    return request.get_json(silent=True) or {}


def _error(code: str, message: str, **kwargs) -> dict:
    payload = {"code": code, "message": message}
    payload.update(kwargs)
    return payload


class ItemListResource(Resource):
    @jwt_required()
    def get(self):
        """Get all items for a kitchen."""
        kitchen_id = request.args.get("kitchen_id", type=int)
        if not kitchen_id:
            return _error("missing_parameter", "kitchen_id parameter is required"), 400

        items = ItemService.get_items_by_kitchen(kitchen_id)
        return {"items": [item.to_dict() for item in items]}, 200

    @jwt_required()
    def post(self):
        """Create a new item."""
        data = _get_json()
        required_fields = ["name", "kitchen_id"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return _error("missing_fields", "Missing required fields", fields=missing), 400

        # Parse status if provided
        status = ItemStatus.IN_STOCK
        if data.get("status"):
            try:
                status = ItemStatus(data["status"])
            except ValueError:
                return _error(
                    "validation_error",
                    "Invalid status. Must be 'needed' or 'in_stock'",
                    field="status",
                ), 400

        item = ItemService.create_item(
            name=data["name"],
            kitchen_id=data["kitchen_id"],
            category=data.get("category"),
            quantity_percent=data.get("quantity_percent", 100.0),
            low_stock_threshold=data.get("low_stock_threshold", 20.0),
            status=status,
        )
        return {"item": item.to_dict()}, 201


class ItemResource(Resource):
    @jwt_required()
    def get(self, item_id: int):
        """Get an item by ID."""
        item = ItemService.get_item_by_id(item_id)
        if not item:
            return _error("not_found", "Item not found"), 404
        return {"item": item.to_dict()}, 200

    @jwt_required()
    def put(self, item_id: int):
        """Update an item."""
        data = _get_json()

        # Parse status if provided
        status = None
        if data.get("status"):
            try:
                status = ItemStatus(data["status"])
            except ValueError:
                return _error(
                    "validation_error",
                    "Invalid status. Must be 'needed' or 'in_stock'",
                    field="status",
                ), 400

        item = ItemService.update_item(
            item_id=item_id,
            name=data.get("name"),
            category=data.get("category"),
            quantity_percent=data.get("quantity_percent"),
            low_stock_threshold=data.get("low_stock_threshold"),
            status=status,
        )
        if not item:
            return _error("not_found", "Item not found"), 404
        return {"item": item.to_dict()}, 200

    @jwt_required()
    def delete(self, item_id: int):
        """Delete an item."""
        success = ItemService.delete_item(item_id)
        if not success:
            return _error("not_found", "Item not found"), 404
        return {"message": "Item deleted successfully"}, 200


class ItemQuantityResource(Resource):
    @jwt_required()
    def patch(self, item_id: int):
        """Update item quantity."""
        data = _get_json()
        quantity_percent = data.get("quantity_percent")

        if quantity_percent is None:
            return _error("missing_fields", "quantity_percent is required"), 400

        if not (0 <= quantity_percent <= 100):
            return _error(
                "validation_error",
                "quantity_percent must be between 0 and 100",
                field="quantity_percent",
            ), 400

        item = ItemService.update_quantity(item_id, quantity_percent)
        if not item:
            return _error("not_found", "Item not found"), 404
        return {"item": item.to_dict()}, 200
