from __future__ import annotations

import secrets

from app.extensions import db
from app.models.kitchen import Kitchen


class KitchenService:
    @staticmethod
    def generate_unique_code() -> str:
        """Generate a unique 6-digit kitchen code."""
        while True:
            code = f"{secrets.randbelow(1000000):06d}"
            if not Kitchen.query.filter_by(code=code).first():
                return code

    @staticmethod
    def create_kitchen(name: str) -> Kitchen:
        """Create a new kitchen with a unique code."""
        code = KitchenService.generate_unique_code()
        kitchen = Kitchen(code=code, name=name)
        db.session.add(kitchen)
        db.session.commit()
        return kitchen

    @staticmethod
    def get_kitchen_by_id(kitchen_id: int) -> Kitchen | None:
        """Get a kitchen by ID."""
        return Kitchen.query.get(kitchen_id)

    @staticmethod
    def get_kitchen_by_code(code: str) -> Kitchen | None:
        """Get a kitchen by its unique code."""
        return Kitchen.query.filter_by(code=code).first()

    @staticmethod
    def get_all_kitchens() -> list[Kitchen]:
        """Get all kitchens."""
        return Kitchen.query.all()

    @staticmethod
    def update_kitchen(kitchen_id: int, name: str) -> Kitchen | None:
        """Update a kitchen's name."""
        kitchen = Kitchen.query.get(kitchen_id)
        if not kitchen:
            return None
        kitchen.name = name
        db.session.commit()
        return kitchen

    @staticmethod
    def delete_kitchen(kitchen_id: int) -> bool:
        """Delete a kitchen."""
        kitchen = Kitchen.query.get(kitchen_id)
        if not kitchen:
            return False
        db.session.delete(kitchen)
        db.session.commit()
        return True
