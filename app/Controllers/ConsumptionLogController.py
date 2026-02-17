from __future__ import annotations

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.Services.ConsumptionLogService import ConsumptionLogService


def _get_json() -> dict:
    return request.get_json(silent=True) or {}


def _error(code: str, message: str, **kwargs) -> dict:
    payload = {"code": code, "message": message}
    payload.update(kwargs)
    return payload


class ConsumptionLogListResource(Resource):
    @jwt_required()
    def get(self):
        """Get consumption logs filtered by item_id, kitchen_id, or user_id."""
        item_id = request.args.get("item_id", type=int)
        kitchen_id = request.args.get("kitchen_id", type=int)
        user_id = request.args.get("user_id", type=int)

        if item_id:
            logs = ConsumptionLogService.get_consumption_logs_by_item(item_id)
        elif kitchen_id:
            logs = ConsumptionLogService.get_consumption_logs_by_kitchen(kitchen_id)
        elif user_id:
            logs = ConsumptionLogService.get_consumption_logs_by_user(user_id)
        else:
            return _error(
                "missing_parameter",
                "One of item_id, kitchen_id, or user_id is required",
            ), 400

        return {"logs": [log.to_dict() for log in logs]}, 200

    @jwt_required()
    def post(self):
        """Create a new consumption log (reduces item quantity)."""
        data = _get_json()
        user_id = int(get_jwt_identity())
        item_id = data.get("item_id")
        percent_used = data.get("percent_used")

        if not item_id or percent_used is None:
            missing = []
            if not item_id:
                missing.append("item_id")
            if percent_used is None:
                missing.append("percent_used")
            return _error("missing_fields", "Missing required fields", fields=missing), 400

        if not (0 <= percent_used <= 100):
            return _error(
                "validation_error",
                "percent_used must be between 0 and 100",
                field="percent_used",
            ), 400

        log = ConsumptionLogService.create_consumption_log(
            user_id=user_id,
            item_id=item_id,
            percent_used=percent_used,
        )
        if not log:
            return _error("not_found", "Item not found"), 404

        return {"log": log.to_dict()}, 201


class ConsumptionLogResource(Resource):
    @jwt_required()
    def get(self, log_id: int):
        """Get a consumption log by ID."""
        log = ConsumptionLogService.get_consumption_log_by_id(log_id)
        if not log:
            return _error("not_found", "Consumption log not found"), 404
        return {"log": log.to_dict()}, 200

    @jwt_required()
    def delete(self, log_id: int):
        """Delete a consumption log."""
        success = ConsumptionLogService.delete_consumption_log(log_id)
        if not success:
            return _error("not_found", "Consumption log not found"), 404
        return {"message": "Consumption log deleted successfully"}, 200
