from flask import request

class ToppingController:
    def __init__(self, topping_service):
        self.topping_service = topping_service
    
    def add_topping(self):
        data = request.get_json()
        topping_name = data.get('topping_name')

        if not topping_name:
            return {"error": "Topping name is required."}
        
        topping_name = topping_name.strip()

        if not all(c.isalpha() or c.isspace() for c in topping_name):
            return {"error": "Topping name must contain only alphabetic characters."}
        
        if len(topping_name) < 1 or len(topping_name) > 100:
            return {"error": "Topping name must be 1 - 100 characters long."}
        
        result = self.topping_service.add_topping(topping_name)
        return result
    
    def get_toppings(self):
        result = self.topping_service.get_toppings()
        return result
    
    def update_topping(self, topping_id):
        data = request.get_json()
        new_topping_name = data.get('new_topping_name')

        if not new_topping_name:
            return {"error": "New topping name is required."}
        
        new_topping_name = new_topping_name.strip()

        if not all(c.isalpha() or c.isspace() for c in new_topping_name):
            return {"error": "New topping name must not contain numbers or special characters."}

        if len(new_topping_name) < 1 or len(new_topping_name) > 100:
            return {"error": "New topping name must be 1 - 100 characters long."}
        
        # Call the service layer to update the topping
        result = self.topping_service.update_topping(topping_id, new_topping_name)
        return result
    
    def delete_topping(self, topping_id):
        if not topping_id or not isinstance(topping_id, str):
            return {"error": "Invalid topping ID. It must be a non-empty string."}

        result = self.topping_service.delete_topping(topping_id)
        return result
