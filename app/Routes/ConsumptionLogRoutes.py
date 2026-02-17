from __future__ import annotations

from flask_restx import Namespace, fields

from app.Controllers.ConsumptionLogController import (
    ConsumptionLogListResource,
    ConsumptionLogResource,
)

consumption_ns = Namespace(
    "consumptions",
    path="/consumptions",
    description="Consumption log endpoints for tracking item usage",
)

consumption_log_model = consumption_ns.model(
    "ConsumptionLog",
    {
        "id": fields.Integer(description="Consumption log ID"),
        "user_id": fields.Integer(description="User who consumed the item"),
        "item_id": fields.Integer(description="Item that was consumed"),
        "percent_used": fields.Float(description="Percentage consumed (0-100)"),
        "created_at": fields.String(description="Timestamp (ISO format)"),
    },
)

create_consumption_log_model = consumption_ns.model(
    "CreateConsumptionLog",
    {
        "item_id": fields.Integer(required=True, description="Item to consume"),
        "percent_used": fields.Float(
            required=True, description="Percentage to consume (0-100)"
        ),
    },
)

consumption_log_list_response = consumption_ns.model(
    "ConsumptionLogListResponse",
    {
        "logs": fields.List(fields.Nested(consumption_log_model)),
    },
)

consumption_log_response = consumption_ns.model(
    "ConsumptionLogResponse",
    {
        "log": fields.Nested(consumption_log_model),
    },
)

error_model = consumption_ns.model(
    "ErrorResponse",
    {
        "code": fields.String(description="Error code"),
        "message": fields.String(description="Error message"),
        "field": fields.String(description="Field that failed validation"),
        "fields": fields.List(fields.String, description="Missing/invalid fields"),
    },
)

auth_header = consumption_ns.parser()
auth_header.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help="Bearer <access_token>",
)


@consumption_ns.route("")
class ConsumptionLogListRoute(ConsumptionLogListResource):
    @consumption_ns.expect(auth_header)
    @consumption_ns.param("item_id", "Filter by item ID", type=int)
    @consumption_ns.param("kitchen_id", "Filter by kitchen ID", type=int)
    @consumption_ns.param("user_id", "Filter by user ID", type=int)
    @consumption_ns.response(200, "Success", consumption_log_list_response)
    @consumption_ns.response(400, "Missing filter parameter", error_model)
    @consumption_ns.response(401, "Unauthorized", error_model)
    def get(self):
        """Get consumption logs (requires one of: item_id, kitchen_id, or user_id)."""
        return super().get()

    @consumption_ns.expect(auth_header, create_consumption_log_model)
    @consumption_ns.response(201, "Consumption log created", consumption_log_response)
    @consumption_ns.response(400, "Validation error", error_model)
    @consumption_ns.response(401, "Unauthorized", error_model)
    @consumption_ns.response(404, "Item not found", error_model)
    def post(self):
        """Create a consumption log (automatically reduces item quantity)."""
        return super().post()


@consumption_ns.route("/<int:log_id>")
class ConsumptionLogRoute(ConsumptionLogResource):
    @consumption_ns.expect(auth_header)
    @consumption_ns.response(200, "Success", consumption_log_response)
    @consumption_ns.response(401, "Unauthorized", error_model)
    @consumption_ns.response(404, "Consumption log not found", error_model)
    def get(self, log_id: int):
        """Get a consumption log by ID."""
        return super().get(log_id)

    @consumption_ns.expect(auth_header)
    @consumption_ns.response(200, "Consumption log deleted")
    @consumption_ns.response(401, "Unauthorized", error_model)
    @consumption_ns.response(404, "Consumption log not found", error_model)
    def delete(self, log_id: int):
        """Delete a consumption log."""
        return super().delete(log_id)
