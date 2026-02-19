from __future__ import annotations

import re

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.models.user_model import User
from app.services.auth_service import AuthService


def _get_json() -> dict:
    return request.get_json(silent=True) or {}


def _error(code: str, message: str, **kwargs) -> dict:
    payload = {"code": code, "message": message}
    payload.update(kwargs)
    return payload


def _is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True


def _is_valid_kitchen_code(code: str) -> bool:
    return bool(re.fullmatch(r"\d{6}", code))


class RegisterResource(Resource):
    def post(self):
        data = _get_json()
        required_fields = ["display_name", "password", "kitchen_code"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return (
                _error(
                    "missing_fields",
                    "Missing required fields",
                    fields=missing,
                ),
                400,
            )

        if not _is_strong_password(data["password"]):
            return (
                _error(
                    "validation_error",
                    "Password must be at least 8 characters and include upper, lower, number, and symbol",
                    field="password",
                ),
                400,
            )

        if not _is_valid_kitchen_code(data["kitchen_code"]):
            return (
                _error(
                    "validation_error",
                    "Kitchen code must be exactly 6 digits",
                    field="kitchen_code",
                ),
                400,
            )

        try:
            user = AuthService.register_user(
                display_name=data["display_name"],
                password=data["password"],
                kitchen_code=data["kitchen_code"],
            )
            tokens = AuthService.generate_tokens(user)
            return {"user": user.to_dict(), **tokens}, 201
        except ValueError as exc:
            return _error("validation_error", str(exc)), 400


class LoginResource(Resource):
    def post(self):
        data = _get_json()
        display_name = data.get("display_name")
        kitchen_code = data.get("kitchen_code")
        password = data.get("password")
        if not display_name or not kitchen_code or not password:
            return (
                _error(
                    "missing_fields",
                    "Missing required fields",
                    fields=["display_name", "kitchen_code", "password"],
                ),
                400,
            )

        if not _is_valid_kitchen_code(kitchen_code):
            return (
                _error(
                    "validation_error",
                    "Kitchen code must be exactly 6 digits",
                    field="kitchen_code",
                ),
                400,
            )

        user = AuthService.authenticate_user(
            display_name=display_name,
            password=password,
            kitchen_code=kitchen_code,
        )
        if not user:
            return _error("auth_invalid_credentials", "Invalid credentials"), 401

        tokens = AuthService.generate_tokens(user)
        return {"user": user.to_dict(), **tokens}, 200


class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = int(get_jwt_identity())
        access_token = AuthService.refresh_access_token(user_id=user_id)
        return {"access_token": access_token}, 200


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return _error("user_not_found", "User not found"), 404
        return {"user": user.to_dict()}, 200
