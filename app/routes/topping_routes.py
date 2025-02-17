from flask import Blueprint, jsonify
from models.db import db
from services.topping_service import ToppingService
from controllers.topping_controller import ToppingController

topping_service = ToppingService(db)
topping_controller = ToppingController(topping_service)

toppings_blueprint = Blueprint('toppings', __name__, url_prefix='/toppings')

# Create (POST) route for adding a new topping
@toppings_blueprint.route('/', methods=['POST'])
def add_topping():
    result = topping_controller.add_topping()
    return jsonify(result), 201 if "error" not in result else 400

# Read (GET) route for fetching all toppings
@toppings_blueprint.route('/', methods=['GET'])
def get_toppings():
    result = topping_controller.get_toppings()
    return jsonify(result), 200

# Update (PUT) route for updating a topping by its ID
@toppings_blueprint.route('/<string:topping_id>', methods=['PUT'])
def update_topping(topping_id):
    result = topping_controller.update_topping(topping_id)
    return jsonify(result), 200 if "error" not in result else 400

# Delete (DELETE) route for deleting a topping by its ID
@toppings_blueprint.route('/<string:topping_id>', methods=['DELETE'])
def delete_topping(topping_id):
    result = topping_controller.delete_topping(topping_id)
    return jsonify(result), 200 if "error" not in result else 400