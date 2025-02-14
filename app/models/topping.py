from models.db import db
import uuid

class Topping(db.Model):
    __tablename__ = "toppings"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Topping {self.name}>"
    