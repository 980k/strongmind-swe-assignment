from flask import request

class PizzaController:
    def __init__(self, pizza_service):
        self.pizza_service = pizza_service

    def validate_name(self, name, name_type="Name"):
        if not name:
            return False, f"{name_type} is required."

        name = name.strip()

        if not all(c.isalpha() or c.isspace() for c in name):
            return False, f"{name_type} must contain only alphabetic characters."

        if len(name) < 1 or len(name) > 100:
            return False, f"{name_type} must be 1 - 100 characters long."

        return True, None  # None means no error, validation is successful

    def add_pizza(self):
        data = request.get_json()
        pizza_name = data.get('pizza_name')
        topping_ids = data.get('topping_ids', [])  # Default to empty list if not provided

        is_valid, error_message = self.validate_name(pizza_name, name_type="Pizza name")

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

        is_valid, error_message = self.validate_name(new_pizza_name, name_type="Pizza name")

        if not is_valid:
            return {"error": error_message}
        
        new_pizza_name = new_pizza_name.strip()

        return self.pizza_service.update_pizza(pizza_id, new_pizza_name, add_topping_ids, remove_topping_ids)
    
    def delete_pizza(self, pizza_id):
        return self.pizza_service.delete_pizza(pizza_id)
