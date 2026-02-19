from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class ConsumptionLog(db.Model):
    __tablename__ = "consumption_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)

    percent_used: Mapped[float] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="consumptions")
    item = relationship("Item", back_populates="consumptions")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_id": self.item_id,
            "percent_used": self.percent_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
