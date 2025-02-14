from flask import Blueprint, request, jsonify
from models.db import db
from models.pizza import Pizza

pizzas_blueprint = Blueprint('pizzas', __name__, url_prefix='/pizzas')

# Create (POST)
@pizzas_blueprint.route('/', methods=['POST'])
def add_pizza():
    data = request.get_json()
    pizza_name = data.get('pizza_name')

    if not pizza_name:
        return jsonify({"error": "Pizza name is required."}), 400
    
    pizza_name = pizza_name.strip()

    existing_pizza = Pizza.query.filter(Pizza.name.ilike(pizza_name)).first()

    if existing_pizza:
        return jsonify({"error": "Pizza already exists."}), 409
    
    new_pizza = Pizza(name=pizza_name)
    db.session.add(new_pizza)
    db.session.commit()

    return jsonify({"id": new_pizza.id, "name": new_pizza.name}), 201

# Read (GET)
@pizzas_blueprint.route('/', methods=['GET'])
def get_pizzas():
        pizzas = Pizza.query.all()
        return jsonify([{'id': pizza.id, 'name': pizza.name} for pizza in pizzas])

# Update (PUT)
@pizzas_blueprint.route('/<int:pizza_id>', methods=['PUT'])
def update_pizza(pizza_id):
    data = request.get_json()
    new_pizza_name = data.get('new_pizza_name')

    if not new_pizza_name:
        return jsonify({"error": "New pizza name is required"}), 400

    pizza = Pizza.query.get(pizza_id)

    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    new_pizza_name = new_pizza_name.strip()

    existing_pizza = Pizza.query.filter(Pizza.name.ilike(new_pizza_name)).first()

    if existing_pizza:
        return jsonify({"error": "Pizza name already exists"}), 400
    
    pizza.name = new_pizza_name
    db.session.commit()

    return jsonify({"id": pizza.id, "name": pizza.name, "message": "Pizza updated"}), 200

# Delete (DELETE)
@pizzas_blueprint.route('/<int:pizza_id>', methods=['DELETE'])
def delete_pizza(pizza_id):
    pizza = Pizza.query.get(pizza_id)

    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    db.session.delete(pizza)
    db.session.commit()

    return '', 204
