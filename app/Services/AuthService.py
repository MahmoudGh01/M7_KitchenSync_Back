from __future__ import annotations

from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import db
from app.Models.UserModel import User
from app.Models.kitchen import Kitchen


class AuthService:
    @staticmethod
    def register_user(display_name: str, password: str, kitchen_code: str) -> User:
        kitchen = Kitchen.query.filter_by(code=kitchen_code).first()
        if not kitchen:
            raise ValueError("Kitchen not found")

        existing = User.query.filter_by(
            display_name=display_name,
            kitchen_id=kitchen.id,
        ).first()
        if existing:
            raise ValueError("Display name already in use for this kitchen")

        user = User(display_name=display_name, kitchen_id=kitchen.id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(
        display_name: str,
        password: str,
        kitchen_code: str,
    ) -> Optional[User]:
        kitchen = Kitchen.query.filter_by(code=kitchen_code).first()
        if not kitchen:
            return None
        user = User.query.filter_by(
            display_name=display_name,
            kitchen_id=kitchen.id,
        ).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def generate_tokens(user: User) -> dict:
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def refresh_access_token(user_id: int) -> str:
        return create_access_token(identity=str(user_id))
