from models.db import db

class PizzaTopping(db.Model):
    __tablename__ = "pizzas_toppings"

    pizza_id = db.Column(db.String(36), db.ForeignKey('pizzas.id'), primary_key=True)
    topping_id = db.Column(db.String(36), db.ForeignKey('toppings.id'), primary_key=True)

    def __repr__(self):
        return f"<PizzaTopping pizza_id={self.pizza_id}, topping_id={self.topping_id}>"
    