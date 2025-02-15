from flask import Blueprint, request, jsonify
from models.db import db
from models.pizza import Pizza
from models.pizza_topping import PizzaTopping
from models.topping import Topping

pizzas_blueprint = Blueprint('pizzas', __name__, url_prefix='/pizzas')

# Create (POST)
@pizzas_blueprint.route('/', methods=['POST'])
def add_pizza():
    data = request.get_json()
    pizza_name = data.get('pizza_name')
    topping_ids = data.get('topping_ids', [])  # Default to empty list if not provided

    if not pizza_name:
        return jsonify({"error": "Pizza name is required."}), 400

    pizza_name = pizza_name.strip()
    existing_pizza = Pizza.query.filter(Pizza.name.ilike(pizza_name)).first()

    if existing_pizza:
        return jsonify({"error": "Pizza already exists."}), 409

    new_pizza = Pizza(name=pizza_name)

    # Attach toppings if provided
    if topping_ids:
        toppings = Topping.query.filter(Topping.id.in_(topping_ids)).all()
        new_pizza.toppings.extend(toppings)  # This is where you link the toppings

    db.session.add(new_pizza)
    db.session.commit()

    return jsonify({
        "id": new_pizza.id,
        "name": new_pizza.name,
        "toppings": [topping.name for topping in new_pizza.toppings]
    }), 201

# Read (GET)
@pizzas_blueprint.route('/', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    
    # Return pizzas and their toppings
    return jsonify([{
        'id': pizza.id,
        'name': pizza.name,
        'toppings': [topping.name for topping in pizza.toppings]  # Access toppings via the relationship
    } for pizza in pizzas])

# Read (GET by ID)
# @pizzas_blueprint.route('/<string:pizza_id>', methods=['GET'])
# def get_pizza(pizza_id):
#     pizza = Pizza.query.get(pizza_id)

#     if not pizza:
#         return jsonify({"error": "Pizza not found"}), 404

#     return jsonify({
#         "id": pizza.id,
#         "name": pizza.name,
#         "toppings": [topping.name for topping in pizza.toppings]  # Convert toppings into a list of names
#     })

# Read (GET by ID)
@pizzas_blueprint.route('/<string:pizza_id>', methods=['GET'])
def get_pizza(pizza_id):
    pizza = Pizza.query.get(pizza_id)

    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    # Return both the topping name and id
    return jsonify({
        "id": pizza.id,
        "name": pizza.name,
        "toppings": [{"id": topping.id, "name": topping.name} for topping in pizza.toppings]  # Include both id and name
    })

# # Update (PUT)
# @pizzas_blueprint.route('/<int:pizza_id>', methods=['PUT'])
# def update_pizza(pizza_id):
#     data = request.get_json()
#     new_pizza_name = data.get('new_pizza_name')

#     if not new_pizza_name:
#         return jsonify({"error": "New pizza name is required"}), 400

#     pizza = Pizza.query.get(pizza_id)

#     if not pizza:
#         return jsonify({"error": "Pizza not found"}), 404

#     new_pizza_name = new_pizza_name.strip()

#     existing_pizza = Pizza.query.filter(Pizza.name.ilike(new_pizza_name)).first()

#     if existing_pizza:
#         return jsonify({"error": "Pizza name already exists"}), 400
    
#     pizza.name = new_pizza_name
#     db.session.commit()

#     return jsonify({"id": pizza.id, "name": pizza.name, "message": "Pizza updated"}), 200

# Update (PUT)
@pizzas_blueprint.route('/<pizza_id>', methods=['PUT'])
def update_pizza(pizza_id):
    data = request.get_json()
    new_name = data.get('pizza_name')
    add_topping_ids = data.get('add_topping_ids', [])
    remove_topping_ids = data.get('remove_topping_ids', [])

    pizza = Pizza.query.get(pizza_id)
    if not pizza:
        return jsonify({"error": "Pizza not found."}), 404

    # Update pizza name if provided
    if new_name:
        new_name = new_name.strip()
        pizza.name = new_name

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

    db.session.commit()

    return jsonify({
        "id": pizza.id,
        "name": pizza.name,
        "toppings": [topping.name for topping in pizza.toppings]
    }), 200

# Delete (DELETE)
@pizzas_blueprint.route('/<int:pizza_id>', methods=['DELETE'])
def delete_pizza(pizza_id):
    pizza = Pizza.query.get(pizza_id)

    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    db.session.delete(pizza)
    db.session.commit()

    return '', 204
