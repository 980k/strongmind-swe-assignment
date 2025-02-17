from models.pizza import Pizza
from models.topping import Topping

class PizzaService:
    def __init__(self, db):
        self.db = db

    def add_pizza(self, pizza_name, topping_ids):
        existing_pizza = Pizza.query.filter(Pizza.name.ilike(pizza_name)).first()

        if existing_pizza:
            return {"error": "Pizza already exists."}

        new_pizza = Pizza(name=pizza_name)

        # Attach toppings if provided
        if topping_ids:
            toppings = Topping.query.filter(Topping.id.in_(topping_ids)).all()
            new_pizza.toppings.extend(toppings)

        self.db.session.add(new_pizza)
        self.db.session.commit()

        return{
            "id": new_pizza.id,
            "name": new_pizza.name,
            "toppings": [topping.name for topping in new_pizza.toppings]
        }
    
    def get_pizzas(self):
        pizzas = Pizza.query.all()

        if not pizzas:
            return []
        
        return [{
        'id': pizza.id,
        'name': pizza.name,
        'toppings': [{'id': topping.id, 'name': topping.name} for topping in pizza.toppings]  # Access toppings via the relationship
        } for pizza in pizzas]
    
    def get_pizza(self, pizza_id):
        pizza = Pizza.query.get(pizza_id)

        if not pizza:
            return {"error": "Pizza not found."}
        
        return {
            "id": pizza.id,
            "name": pizza.name,
            "toppings": [{"id": topping.id, "name": topping.name} for topping in pizza.toppings]  # Include both id and name
        }
    
    def update_pizza(self, pizza_id, new_pizza_name, add_topping_ids, remove_topping_ids):
        pizza = Pizza.query.get(pizza_id)

        if not pizza:
            return {"error": "Pizza not found."}
        
        # Set new name
        pizza.name = new_pizza_name

        # Remove toppings
        if remove_topping_ids:
            toppings_to_remove = Topping.query.filter(Topping.id.in_(remove_topping_ids)).all()
            for topping in toppings_to_remove:
                if topping in pizza.toppings:
                    pizza.toppings.remove(topping)

        # Add new toppings
        if add_topping_ids:
            toppings_to_add = Topping.query.filter(Topping.id.in_(add_topping_ids)).all()
            pizza.toppings.extend(toppings_to_add)

        self.db.session.commit()

        return {
            "id": pizza.id,
            "name": pizza.name,
            "toppings": [topping.name for topping in pizza.toppings]
        }
    
    def delete_pizza(self, pizza_id):
        pizza = Pizza.query.get(pizza_id)

        if not pizza:
            return {"error": "Pizza not found."}
        
        # Explicitly remove all toppings before deleting the pizza
        toppings = pizza.toppings.all()
        for topping in toppings:
            pizza.toppings.remove(topping)

        self.db.session.delete(pizza)
        self.db.session.commit()

        return {"message": "Pizza deleted successfully."}
