from __future__ import annotations

from flask_restx import Namespace, fields

from app.Controllers.AuthController import (
    LoginResource,
    MeResource,
    RefreshResource,
    RegisterResource,
)

auth_ns = Namespace("auth", path="/auth", description="Authentication")

register_model = auth_ns.model(
    "RegisterRequest",
    {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

login_model = auth_ns.model(
    "LoginRequest",
    {
        "identity": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

@auth_ns.route("/register")
class RegisterRoute(RegisterResource):
    @auth_ns.expect(register_model)
    def post(self):
        return super().post()


@auth_ns.route("/login")
class LoginRoute(LoginResource):
    @auth_ns.expect(login_model)
    def post(self):
        return super().post()


@auth_ns.route("/refresh")
class RefreshRoute(RefreshResource):
    def post(self):
        return super().post()


@auth_ns.route("/me")
class MeRoute(MeResource):
    def get(self):
        return super().get()
