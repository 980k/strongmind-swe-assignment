from flask import request
from helpers.validators import validate_name

class ToppingController:
    def __init__(self, topping_service):
        self.topping_service = topping_service
    
    def add_topping(self):
        data = request.get_json()
        topping_name = data.get('topping_name')

        # Validate topping name
        is_valid, error_message = validate_name(topping_name, name_type="Topping name")
        
        if not is_valid:
            return {"error": error_message}

        topping_name = topping_name.strip()
        
        result = self.topping_service.add_topping(topping_name)
        return result
    
    def get_toppings(self):
        result = self.topping_service.get_toppings()
        return result
    
    def update_topping(self, topping_id):
        data = request.get_json()
        new_topping_name = data.get('new_topping_name')

        # Validate new topping name
        is_valid, error_message = validate_name(new_topping_name, name_type="New topping name")
        
        if not is_valid:
            return {"error": error_message}

        new_topping_name = new_topping_name.strip()

        result = self.topping_service.update_topping(topping_id, new_topping_name)
        return result
    
    def delete_topping(self, topping_id):
        if not topping_id or not isinstance(topping_id, str):
            return {"error": "Invalid topping ID. It must be a non-empty string."}

        result = self.topping_service.delete_topping(topping_id)
        return result
