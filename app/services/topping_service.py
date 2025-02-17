from models.topping import Topping

class ToppingService:
    def __init__(self, db):
        self.db = db

    def add_topping(self, topping_name):
        # Check if topping already exists (case-insensitive)
        existing_topping = Topping.query.filter(Topping.name.ilike(topping_name)).first()

        if existing_topping:
            return {"error": "Topping already exists."}

        # Create new topping
        new_topping = Topping(name=topping_name)
        self.db.session.add(new_topping)
        self.db.session.commit()

        return {"message": "Topping created.","id": new_topping.id, "name": new_topping.name}

    def get_toppings(self):
        toppings = Topping.query.all()  # Query all toppings from the database

        if not toppings:
            return []

        return [{'id': topping.id, 'name': topping.name} for topping in toppings]
    
    def update_topping(self, topping_id, new_topping_name):
        topping = Topping.query.get(topping_id)

        if not topping:
            return {"error": "Topping not found."}
        
        # prevents update if a topping already exists
        existing_topping_name = Topping.query.filter(Topping.name.ilike(new_topping_name)).first()

        if existing_topping_name:
            return {"error": "Topping name already exists."}
        
        topping.name = new_topping_name
        self.db.session.commit()

        return {"message": "Topping updated.","id": topping.id, "name": topping.name}

    def delete_topping(self, topping_id):
        topping = Topping.query.get(topping_id)

        if not topping:
            return {"error": "Topping not found."}
        
        self.db.session.delete(topping)
        self.db.session.commit()

        return {"message": "Topping deleted successfully."}
