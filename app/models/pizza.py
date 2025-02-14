from models.db import db
import uuid

class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Pizza {self.name}>"
    