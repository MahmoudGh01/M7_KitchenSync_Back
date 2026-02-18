from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

class Kitchen(db.Model):
    __tablename__ = "kitchens"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False,
        index=True
    )  # Unique 6-digit room code

    name: Mapped[str] = mapped_column(String(120), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    users = relationship("User", back_populates="kitchen")
    items = relationship("Item", back_populates="kitchen")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
