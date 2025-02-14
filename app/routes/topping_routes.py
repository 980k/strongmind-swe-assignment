from flask import Blueprint, request, jsonify
from models.db import db
from models.topping import Topping

toppings_blueprint = Blueprint('toppings', __name__, url_prefix='/toppings')

# Create (POST)
@toppings_blueprint.route('/add_topping', methods=['POST'])
def add_topping():
    data = request.get_json()  # Use get_json() instead of request.json()

    topping_name = data.get('topping_name')

    if not topping_name:
        return jsonify({"error": "Topping name is required"}), 400
    
    topping_name = topping_name.strip()  # Strip and lower the name correctly

    # Check if the topping already exists (comparison is case-insensitive)
    existing_topping = Topping.query.filter(Topping.name.ilike(topping_name)).first()

    if existing_topping:
        return jsonify({"error": "Topping already exists"}), 400

    # Create the topping and add it to the database
    new_topping = Topping(name=topping_name)
    db.session.add(new_topping)
    db.session.commit()

    return jsonify({"message": "Topping added", "topping": new_topping.name}), 201

# Read (GET)
@toppings_blueprint.route('/get_toppings', methods=['GET'])
def get_toppings():
    toppings = Topping.query.all()  # Query all toppings from the database
    return jsonify([{'id': topping.id, 'name': topping.name} for topping in toppings])  # Include both id and name

# Update (PUT)
@toppings_blueprint.route('/update_topping/<topping_name>', methods=['PUT'])
def update_topping(topping_name):
    data = request.get_json()
    new_topping_name = data.get('new_topping_name')

    if not new_topping_name:
        return jsonify({"error": "New topping name is required."}), 400

    # Check if the topping exists
    topping = Topping.query.filter(Topping.name.ilike(topping_name)).first()

    if not topping:
        return jsonify({"error": "Topping not found."}), 404
    
    new_topping_name = new_topping_name.strip()

    # Check if the new topping name already exists
    existing_topping = Topping.query.filter(Topping.name.ilike(new_topping_name)).first()
    if existing_topping:
        return jsonify({"error": "Topping name already exists."}), 400

    # Update the topping
    topping.name = new_topping_name
    db.session.commit()

    return jsonify({"message": "Topping updated", "topping": topping.name}), 200

# Delete (DELETE)
@toppings_blueprint.route('/delete_topping/<topping_name>', methods=['DELETE'])
def delete_topping(topping_name):
    topping = Topping.query.filter(Topping.name.ilike(topping_name)).first()

    if not topping:
        return jsonify({"error": "Topping does not exist."}), 404
    
    db.session.delete(topping)
    db.session.commit()

    return jsonify({"message": "Topping deleted successfully."}), 200
