from __future__ import annotations

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.Services.RestockLogService import RestockLogService


def _get_json() -> dict:
    return request.get_json(silent=True) or {}


def _error(code: str, message: str, **kwargs) -> dict:
    payload = {"code": code, "message": message}
    payload.update(kwargs)
    return payload


class RestockLogListResource(Resource):
    @jwt_required()
    def get(self):
        """Get restock logs filtered by item_id, kitchen_id, or user_id."""
        item_id = request.args.get("item_id", type=int)
        kitchen_id = request.args.get("kitchen_id", type=int)
        user_id = request.args.get("user_id", type=int)

        if item_id:
            logs = RestockLogService.get_restock_logs_by_item(item_id)
        elif kitchen_id:
            logs = RestockLogService.get_restock_logs_by_kitchen(kitchen_id)
        elif user_id:
            logs = RestockLogService.get_restock_logs_by_user(user_id)
        else:
            return _error(
                "missing_parameter",
                "One of item_id, kitchen_id, or user_id is required",
            ), 400

        return {"logs": [log.to_dict() for log in logs]}, 200

    @jwt_required()
    def post(self):
        """Create a new restock log (restocks item to 100%)."""
        data = _get_json()
        user_id = int(get_jwt_identity())
        item_id = data.get("item_id")

        if not item_id:
            return _error("missing_fields", "item_id is required"), 400

        log = RestockLogService.create_restock_log(user_id=user_id, item_id=item_id)
        if not log:
            return _error("not_found", "Item not found"), 404

        return {"log": log.to_dict()}, 201


class RestockLogResource(Resource):
    @jwt_required()
    def get(self, log_id: int):
        """Get a restock log by ID."""
        log = RestockLogService.get_restock_log_by_id(log_id)
        if not log:
            return _error("not_found", "Restock log not found"), 404
        return {"log": log.to_dict()}, 200

    @jwt_required()
    def delete(self, log_id: int):
        """Delete a restock log."""
        success = RestockLogService.delete_restock_log(log_id)
        if not success:
            return _error("not_found", "Restock log not found"), 404
        return {"message": "Restock log deleted successfully"}, 200
