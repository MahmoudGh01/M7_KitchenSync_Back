import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class ItemStatus(enum.Enum):
    NEEDED = "needed"
    IN_STOCK = "in_stock"


class Item(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(120), nullable=False)

    category: Mapped[str] = mapped_column(String(80), nullable=True)

    quantity_percent: Mapped[float] = mapped_column(default=100.0)

    low_stock_threshold: Mapped[float] = mapped_column(default=20.0)

    status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus), default=ItemStatus.NEEDED)

    kitchen_id: Mapped[int] = mapped_column(ForeignKey("kitchens.id"), nullable=False)

    kitchen = relationship("Kitchen", back_populates="items")
    restocks = relationship("RestockLog", back_populates="item")
    consumptions = relationship("ConsumptionLog", back_populates="item")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "quantity_percent": self.quantity_percent,
            "low_stock_threshold": self.low_stock_threshold,
            "status": self.status.value if self.status else None,
            "kitchen_id": self.kitchen_id,
        }
