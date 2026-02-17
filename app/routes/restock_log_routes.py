from __future__ import annotations

from flask_restx import Namespace, fields

from app.controllers.restock_log_controller import (
    RestockLogListResource,
    RestockLogResource,
)

restock_ns = Namespace(
    "restocks",
    path="/restocks",
    description="Restock log endpoints for tracking when items are restocked",
)

restock_log_model = restock_ns.model(
    "RestockLog",
    {
        "id": fields.Integer(description="Restock log ID"),
        "user_id": fields.Integer(description="User who restocked the item"),
        "item_id": fields.Integer(description="Item that was restocked"),
        "created_at": fields.String(description="Timestamp (ISO format)"),
    },
)

create_restock_log_model = restock_ns.model(
    "CreateRestockLog",
    {
        "item_id": fields.Integer(required=True, description="Item to restock"),
    },
)

restock_log_list_response = restock_ns.model(
    "RestockLogListResponse",
    {
        "logs": fields.List(fields.Nested(restock_log_model)),
    },
)

restock_log_response = restock_ns.model(
    "RestockLogResponse",
    {
        "log": fields.Nested(restock_log_model),
    },
)

error_model = restock_ns.model(
    "ErrorResponse",
    {
        "code": fields.String(description="Error code"),
        "message": fields.String(description="Error message"),
        "field": fields.String(description="Field that failed validation"),
    },
)

auth_header = restock_ns.parser()
auth_header.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help="Bearer <access_token>",
)


@restock_ns.route("")
class RestockLogListRoute(RestockLogListResource):
    @restock_ns.expect(auth_header)
    @restock_ns.param("item_id", "Filter by item ID", type=int)
    @restock_ns.param("kitchen_id", "Filter by kitchen ID", type=int)
    @restock_ns.param("user_id", "Filter by user ID", type=int)
    @restock_ns.response(200, "Success", restock_log_list_response)
    @restock_ns.response(400, "Missing filter parameter", error_model)
    @restock_ns.response(401, "Unauthorized", error_model)
    def get(self):
        """Get restock logs (requires one of: item_id, kitchen_id, or user_id)."""
        return super().get()

    @restock_ns.expect(auth_header, create_restock_log_model)
    @restock_ns.response(201, "Restock log created", restock_log_response)
    @restock_ns.response(400, "Validation error", error_model)
    @restock_ns.response(401, "Unauthorized", error_model)
    @restock_ns.response(404, "Item not found", error_model)
    def post(self):
        """Create a restock log (automatically sets item to 100% stock)."""
        return super().post()


@restock_ns.route("/<int:log_id>")
class RestockLogRoute(RestockLogResource):
    @restock_ns.expect(auth_header)
    @restock_ns.response(200, "Success", restock_log_response)
    @restock_ns.response(401, "Unauthorized", error_model)
    @restock_ns.response(404, "Restock log not found", error_model)
    def get(self, log_id: int):
        """Get a restock log by ID."""
        return super().get(log_id)

    @restock_ns.expect(auth_header)
    @restock_ns.response(200, "Restock log deleted")
    @restock_ns.response(401, "Unauthorized", error_model)
    @restock_ns.response(404, "Restock log not found", error_model)
    def delete(self, log_id: int):
        """Delete a restock log."""
        return super().delete(log_id)
