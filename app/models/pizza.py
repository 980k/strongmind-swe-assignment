from models.db import db
import uuid

class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Define the relationship with the Topping model using the class reference
    toppings = db.relationship(
        'Topping',  # Target model
        secondary='pizzas_toppings',  # Table name is automatically inferred here
        backref='pizzas',  # This allows access to pizzas from the Topping model
        lazy='dynamic'  # Optionally set how you want to load related items (e.g., lazy or joined)
    )

    def __repr__(self):
        return f"<Pizza {self.name}>"
    