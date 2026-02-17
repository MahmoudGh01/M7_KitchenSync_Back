from __future__ import annotations

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.Services.KitchenService import KitchenService


def _get_json() -> dict:
    return request.get_json(silent=True) or {}


def _error(code: str, message: str, **kwargs) -> dict:
    payload = {"code": code, "message": message}
    payload.update(kwargs)
    return payload


class KitchenListResource(Resource):
    def get(self):
        """Get all kitchens."""
        kitchens = KitchenService.get_all_kitchens()
        return {"kitchens": [k.to_dict() for k in kitchens]}, 200

    def post(self):
        """Create a new kitchen."""
        data = _get_json()
        name = data.get("name")
        if not name:
            return _error("missing_fields", "Missing required field", field="name"), 400

        kitchen = KitchenService.create_kitchen(name=name)
        return {"kitchen": kitchen.to_dict()}, 201


class KitchenResource(Resource):
    def get(self, kitchen_id: int):
        """Get a kitchen by ID."""
        kitchen = KitchenService.get_kitchen_by_id(kitchen_id)
        if not kitchen:
            return _error("not_found", "Kitchen not found"), 404
        return {"kitchen": kitchen.to_dict()}, 200

    def put(self, kitchen_id: int):
        """Update a kitchen's name."""
        data = _get_json()
        name = data.get("name")
        if not name:
            return _error("missing_fields", "Missing required field", field="name"), 400

        kitchen = KitchenService.update_kitchen(kitchen_id, name)
        if not kitchen:
            return _error("not_found", "Kitchen not found"), 404
        return {"kitchen": kitchen.to_dict()}, 200

    def delete(self, kitchen_id: int):
        """Delete a kitchen."""
        success = KitchenService.delete_kitchen(kitchen_id)
        if not success:
            return _error("not_found", "Kitchen not found"), 404
        return {"message": "Kitchen deleted successfully"}, 200


class KitchenByCodeResource(Resource):
    def get(self, code: str):
        """Get a kitchen by its unique code."""
        kitchen = KitchenService.get_kitchen_by_code(code)
        if not kitchen:
            return _error("not_found", "Kitchen not found"), 404
        return {"kitchen": kitchen.to_dict()}, 200
