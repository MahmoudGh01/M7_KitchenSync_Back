# models/user.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔹 Password setter
    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)

    # 🔹 Password verifier
    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    # 🔹 Serialize user
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
