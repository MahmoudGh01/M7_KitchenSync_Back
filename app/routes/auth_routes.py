from __future__ import annotations

from flask_restx import Namespace, fields

from app.controllers.auth_controller import (
    LoginResource,
    MeResource,
    RefreshResource,
    RegisterResource,
)

auth_ns = Namespace(
    "auth",
    path="/auth",
    description=(
        "Authentication endpoints using JWT access/refresh tokens. "
        "Use the access token for protected resources and the refresh token "
        "to obtain a new access token when it expires."
    ),
)

register_model = auth_ns.model(
    "RegisterRequest",
    {
        "display_name": fields.String(
            required=True,
            description="Display name for the user",
        ),
        "kitchen_code": fields.String(
            required=True,
            description="6-digit kitchen code",
        ),
        "password": fields.String(
            required=True,
            description=(
                "Password must be at least 8 characters and include upper, lower, number, and symbol"
            ),
        ),
    },
)

login_model = auth_ns.model(
    "LoginRequest",
    {
        "display_name": fields.String(
            required=True,
            description="User display name",
        ),
        "kitchen_code": fields.String(
            required=True,
            description="6-digit kitchen code",
        ),
        "password": fields.String(required=True, description="Account password"),
    },
)

user_model = auth_ns.model(
    "User",
    {
        "id": fields.Integer(description="User id"),
        "display_name": fields.String(description="Display name"),
        "kitchen_id": fields.Integer(description="Kitchen id"),
        "kitchen_code": fields.String(description="Kitchen code"),
        "is_active": fields.Boolean(description="Active status"),
    },
)

token_model = auth_ns.model(
    "TokenPair",
    {
        "access_token": fields.String(description="JWT access token"),
        "refresh_token": fields.String(description="JWT refresh token"),
    },
)

access_token_model = auth_ns.model(
    "AccessToken",
    {
        "access_token": fields.String(description="JWT access token"),
    },
)

register_response_model = auth_ns.model(
    "RegisterResponse",
    {
        "user": fields.Nested(user_model),
        "access_token": fields.String(description="JWT access token"),
        "refresh_token": fields.String(description="JWT refresh token"),
    },
)

login_response_model = auth_ns.clone(
    "LoginResponse",
    register_response_model,
)

me_response_model = auth_ns.model(
    "MeResponse",
    {
        "user": fields.Nested(user_model),
    },
)

error_model = auth_ns.model(
    "ErrorResponse",
    {
        "code": fields.String(description="Error code"),
        "message": fields.String(description="Human-readable error message"),
        "field": fields.String(description="Field that failed validation"),
        "fields": fields.List(fields.String, description="Missing/invalid fields"),
    },
)

auth_header = auth_ns.parser()
auth_header.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help="Bearer <token>",
)


@auth_ns.route("/register")
class RegisterRoute(RegisterResource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, "User registered", register_response_model)
    @auth_ns.response(400, "Validation error", error_model)
    def post(self):
        """Create a new user account."""
        return super().post()


@auth_ns.route("/login")
class LoginRoute(LoginResource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, "Authenticated", login_response_model)
    @auth_ns.response(400, "Validation error", error_model)
    @auth_ns.response(401, "Invalid credentials", error_model)
    def post(self):
        """Authenticate with display name, kitchen code, and password."""
        return super().post()


@auth_ns.route("/refresh")
class RefreshRoute(RefreshResource):
    @auth_ns.expect(auth_header)
    @auth_ns.response(200, "Access token refreshed", access_token_model)
    @auth_ns.response(401, "Invalid or expired refresh token", error_model)
    def post(self):
        """Refresh access token using a refresh token."""
        return super().post()


@auth_ns.route("/me")
class MeRoute(MeResource):
    @auth_ns.expect(auth_header)
    @auth_ns.response(200, "Current user", me_response_model)
    @auth_ns.response(401, "Missing or invalid access token", error_model)
    @auth_ns.response(404, "User not found", error_model)
    def get(self):
        """Get the current authenticated user."""
        return super().get()
