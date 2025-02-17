from models.db import db
import uuid

class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Defines a many-to-many relationship between Pizza and Topping through the 
    # pizzas_toppings association table.
    toppings = db.relationship(
        'Topping',
        secondary='pizzas_toppings',
        backref='pizzas',
        lazy='dynamic'
    )

    def __repr__(self):
        return f"<Pizza {self.name}>"
    