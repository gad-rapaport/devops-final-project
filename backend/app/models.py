from datetime import datetime
from app import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    nutritional_info = db.Column(db.Text, nullable=True)
    cuisine_type = db.Column(db.String(100), nullable=True)
    prep_time_minutes = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "nutritional_info": self.nutritional_info,
            "cuisine_type": self.cuisine_type,
            "prep_time_minutes": self.prep_time_minutes,
            "rating": self.rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
