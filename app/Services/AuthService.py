from __future__ import annotations

from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token

from app.Models.UserModel import User, db


class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing:
            raise ValueError("Username or email already in use")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(identity: str, password: str) -> Optional[User]:
        user = User.query.filter(
            (User.email == identity) | (User.username == identity)
        ).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user

    @staticmethod
    def generate_tokens(user: User) -> dict:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def refresh_access_token(user_id: int) -> str:
        return create_access_token(identity=user_id)
