from flask import Blueprint, jsonify
from models.db import db
from services.topping_service import ToppingService
from controllers.topping_controller import ToppingController

topping_service = ToppingService(db)
topping_controller = ToppingController(topping_service)

toppings_blueprint = Blueprint('toppings', __name__, url_prefix='/toppings')

# Create (POST)
@toppings_blueprint.route('/', methods=['POST'])
def add_topping():
    result = topping_controller.add_topping()
    return jsonify(result), 201 if "error" not in result else 400

# Read (GET)
@toppings_blueprint.route('/', methods=['GET'])
def get_toppings():
    result = topping_controller.get_toppings()
    return jsonify(result), 200

# Update (PUT)
@toppings_blueprint.route('/<string:topping_id>', methods=['PUT'])
def update_topping(topping_id):
    result = topping_controller.update_topping(topping_id)
    return jsonify(result), 200 if "error" not in result else 400

# Delete (DELETE)
@toppings_blueprint.route('/<string:topping_id>', methods=['DELETE'])
def delete_topping(topping_id):
    result = topping_controller.delete_topping(topping_id)
    return jsonify(result), 200 if "error" not in result else 400