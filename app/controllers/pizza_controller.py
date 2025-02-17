from flask import request
from helpers.validators import validate_name

class PizzaController:
    def __init__(self, pizza_service):
        self.pizza_service = pizza_service

    def add_pizza(self):
        data = request.get_json()
        pizza_name = data.get('pizza_name')
        topping_ids = data.get('topping_ids', [])  # Default to empty list if not provided

        # Validate pizza name
        is_valid, error_message = validate_name(pizza_name, name_type="Pizza name")

        if not is_valid:
            return {"error": error_message}
        
        pizza_name = pizza_name.strip()
        
        return self.pizza_service.add_pizza(pizza_name, topping_ids)
    
    def get_pizzas(self):
        return self.pizza_service.get_pizzas()
    
    def get_pizza(self, pizza_id):
        return self.pizza_service.get_pizza(pizza_id)
    
    def update_pizza(self, pizza_id):
        data = request.get_json()
        new_pizza_name = data.get('pizza_name')
        add_topping_ids = data.get('add_topping_ids', [])
        remove_topping_ids = data.get('remove_topping_ids', [])

        # Validate new pizza name
        is_valid, error_message = validate_name(new_pizza_name, name_type="Pizza name")

        if not is_valid:
            return {"error": error_message}
        
        new_pizza_name = new_pizza_name.strip()

        return self.pizza_service.update_pizza(pizza_id, new_pizza_name, add_topping_ids, remove_topping_ids)
    
    def delete_pizza(self, pizza_id):
        return self.pizza_service.delete_pizza(pizza_id)
