from __future__ import annotations

from flask_restx import Namespace, fields

from app.controllers.item_controller import (
    ItemListResource,
    ItemQuantityResource,
    ItemResource,
)

item_ns = Namespace(
    "items",
    path="/items",
    description="Item management endpoints for tracking kitchen inventory",
)

item_model = item_ns.model(
    "Item",
    {
        "id": fields.Integer(description="Item ID"),
        "name": fields.String(description="Item name"),
        "category": fields.String(description="Item category"),
        "quantity_percent": fields.Float(description="Quantity as percentage (0-100)"),
        "low_stock_threshold": fields.Float(description="Low stock threshold percentage"),
        "status": fields.String(description="Item status (needed, in_stock)"),
        "kitchen_id": fields.Integer(description="Kitchen ID"),
    },
)

create_item_model = item_ns.model(
    "CreateItem",
    {
        "name": fields.String(required=True, description="Item name"),
        "kitchen_id": fields.Integer(required=True, description="Kitchen ID"),
        "category": fields.String(description="Item category"),
        "quantity_percent": fields.Float(description="Quantity as percentage (default: 100.0)"),
        "low_stock_threshold": fields.Float(description="Low stock threshold (default: 20.0)"),
        "status": fields.String(
            description="Item status: 'needed' or 'in_stock' (default: in_stock)"
        ),
    },
)

update_item_model = item_ns.model(
    "UpdateItem",
    {
        "name": fields.String(description="Item name"),
        "category": fields.String(description="Item category"),
        "quantity_percent": fields.Float(description="Quantity as percentage (0-100)"),
        "low_stock_threshold": fields.Float(description="Low stock threshold"),
        "status": fields.String(description="Item status: 'needed' or 'in_stock'"),
    },
)

update_quantity_model = item_ns.model(
    "UpdateQuantity",
    {
        "quantity_percent": fields.Float(
            required=True, description="Quantity as percentage (0-100)"
        ),
    },
)

item_list_response = item_ns.model(
    "ItemListResponse",
    {
        "items": fields.List(fields.Nested(item_model)),
    },
)

item_response = item_ns.model(
    "ItemResponse",
    {
        "item": fields.Nested(item_model),
    },
)

error_model = item_ns.model(
    "ErrorResponse",
    {
        "code": fields.String(description="Error code"),
        "message": fields.String(description="Error message"),
        "field": fields.String(description="Field that failed validation"),
        "fields": fields.List(fields.String, description="Missing/invalid fields"),
    },
)

auth_header = item_ns.parser()
auth_header.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help="Bearer <access_token>",
)


@item_ns.route("")
class ItemListRoute(ItemListResource):
    @item_ns.expect(auth_header)
    @item_ns.param("kitchen_id", "Kitchen ID", type=int, required=True)
    @item_ns.response(200, "Success", item_list_response)
    @item_ns.response(400, "Missing kitchen_id parameter", error_model)
    @item_ns.response(401, "Unauthorized", error_model)
    def get(self):
        """Get all items for a kitchen."""
        return super().get()

    @item_ns.expect(auth_header, create_item_model)
    @item_ns.response(201, "Item created", item_response)
    @item_ns.response(400, "Validation error", error_model)
    @item_ns.response(401, "Unauthorized", error_model)
    def post(self):
        """Create a new item."""
        return super().post()


@item_ns.route("/<int:item_id>")
class ItemRoute(ItemResource):
    @item_ns.expect(auth_header)
    @item_ns.response(200, "Success", item_response)
    @item_ns.response(401, "Unauthorized", error_model)
    @item_ns.response(404, "Item not found", error_model)
    def get(self, item_id: int):
        """Get an item by ID."""
        return super().get(item_id)

    @item_ns.expect(auth_header, update_item_model)
    @item_ns.response(200, "Item updated", item_response)
    @item_ns.response(400, "Validation error", error_model)
    @item_ns.response(401, "Unauthorized", error_model)
    @item_ns.response(404, "Item not found", error_model)
    def put(self, item_id: int):
        """Update an item."""
        return super().put(item_id)

    @item_ns.expect(auth_header)
    @item_ns.response(200, "Item deleted")
    @item_ns.response(401, "Unauthorized", error_model)
    @item_ns.response(404, "Item not found", error_model)
    def delete(self, item_id: int):
        """Delete an item."""
        return super().delete(item_id)


@item_ns.route("/<int:item_id>/quantity")
class ItemQuantityRoute(ItemQuantityResource):
    @item_ns.expect(auth_header, update_quantity_model)
    @item_ns.response(200, "Quantity updated", item_response)
    @item_ns.response(400, "Validation error", error_model)
    @item_ns.response(401, "Unauthorized", error_model)
    @item_ns.response(404, "Item not found", error_model)
    def patch(self, item_id: int):
        """Update item quantity and auto-adjust status."""
        return super().patch(item_id)
