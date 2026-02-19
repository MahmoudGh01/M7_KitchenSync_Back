from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    display_name: Mapped[str] = mapped_column(String(80), nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    kitchen_id: Mapped[int] = mapped_column(ForeignKey("kitchens.id"), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    kitchen = relationship("Kitchen", back_populates="users")
    restocks = relationship("RestockLog", back_populates="user")
    consumptions = relationship("ConsumptionLog", back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "kitchen_id": self.kitchen_id,
            "kitchen_code": self.kitchen.code if self.kitchen else None,
            "is_active": self.is_active,
        }
