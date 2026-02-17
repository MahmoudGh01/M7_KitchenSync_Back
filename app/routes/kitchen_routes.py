from __future__ import annotations

from flask_restx import Namespace, fields

from app.controllers.kitchen_controller import (
    KitchenListResource,
    KitchenResource,
    KitchenByCodeResource,
)

kitchen_ns = Namespace(
    "kitchens",
    path="/kitchens",
    description="Kitchen management endpoints for creating and managing shared kitchens",
)

kitchen_model = kitchen_ns.model(
    "Kitchen",
    {
        "id": fields.Integer(description="Kitchen ID"),
        "code": fields.String(description="Unique 6-digit kitchen code"),
        "name": fields.String(description="Kitchen name"),
        "created_at": fields.String(description="Creation timestamp (ISO format)"),
    },
)

create_kitchen_model = kitchen_ns.model(
    "CreateKitchen",
    {
        "name": fields.String(required=True, description="Kitchen name"),
    },
)

update_kitchen_model = kitchen_ns.model(
    "UpdateKitchen",
    {
        "name": fields.String(required=True, description="Kitchen name"),
    },
)

kitchen_list_response = kitchen_ns.model(
    "KitchenListResponse",
    {
        "kitchens": fields.List(fields.Nested(kitchen_model)),
    },
)

kitchen_response = kitchen_ns.model(
    "KitchenResponse",
    {
        "kitchen": fields.Nested(kitchen_model),
    },
)

error_model = kitchen_ns.model(
    "ErrorResponse",
    {
        "code": fields.String(description="Error code"),
        "message": fields.String(description="Error message"),
        "field": fields.String(description="Field that failed validation"),
    },
)


@kitchen_ns.route("")
class KitchenListRoute(KitchenListResource):
    @kitchen_ns.response(200, "Success", kitchen_list_response)
    def get(self):
        """Get all kitchens."""
        return super().get()

    @kitchen_ns.expect(create_kitchen_model)
    @kitchen_ns.response(201, "Kitchen created", kitchen_response)
    @kitchen_ns.response(400, "Validation error", error_model)
    def post(self):
        """Create a new kitchen with a unique code."""
        return super().post()


@kitchen_ns.route("/<int:kitchen_id>")
class KitchenRoute(KitchenResource):
    @kitchen_ns.response(200, "Success", kitchen_response)
    @kitchen_ns.response(404, "Kitchen not found", error_model)
    def get(self, kitchen_id: int):
        """Get a kitchen by ID."""
        return super().get(kitchen_id)

    @kitchen_ns.expect(update_kitchen_model)
    @kitchen_ns.response(200, "Kitchen updated", kitchen_response)
    @kitchen_ns.response(400, "Validation error", error_model)
    @kitchen_ns.response(404, "Kitchen not found", error_model)
    def put(self, kitchen_id: int):
        """Update a kitchen's name."""
        return super().put(kitchen_id)

    @kitchen_ns.response(200, "Kitchen deleted")
    @kitchen_ns.response(404, "Kitchen not found", error_model)
    def delete(self, kitchen_id: int):
        """Delete a kitchen."""
        return super().delete(kitchen_id)


@kitchen_ns.route("/code/<string:code>")
class KitchenByCodeRoute(KitchenByCodeResource):
    @kitchen_ns.response(200, "Success", kitchen_response)
    @kitchen_ns.response(404, "Kitchen not found", error_model)
    def get(self, code: str):
        """Get a kitchen by its unique 6-digit code."""
        return super().get(code)
