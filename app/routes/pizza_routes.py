from flask import Blueprint, jsonify
from models.db import db
from services.pizza_service import PizzaService
from controllers.pizza_controller import PizzaController
from auth.auth import auth

pizza_service = PizzaService(db)
pizza_controller = PizzaController(pizza_service)

pizzas_blueprint = Blueprint('pizzas', __name__, url_prefix='/pizzas')

# Create (POST) route for adding a new pizza
@pizzas_blueprint.route('/', methods=['POST'])
@auth.login_required
def add_pizza():
    result = pizza_controller.add_pizza()
    return jsonify(result), 201 if "error" not in result else 400

# Read (GET) route for fetching all pizzas
@pizzas_blueprint.route('/', methods=['GET'])
@auth.login_required
def get_pizzas():
    result = pizza_controller.get_pizzas()
    return jsonify(result), 200 if "error" not in result else 400

# Read (GET) route for fetching a pizza by its ID
@pizzas_blueprint.route('/<string:pizza_id>', methods=['GET'])
@auth.login_required
def get_pizza(pizza_id):
    result = pizza_controller.get_pizza(pizza_id)
    return jsonify(result), 200 if "error" not in result else 400

# Update (PUT) route for updating a pizza by its ID
@pizzas_blueprint.route('/<string:pizza_id>', methods=['PUT'])
@auth.login_required
def update_pizza(pizza_id):
    result = pizza_controller.update_pizza(pizza_id)
    return jsonify(result), 200 if "error" not in result else 400

# Delete (DELETE) route for deleting a pizza by its ID
@pizzas_blueprint.route('/<string:pizza_id>', methods=['DELETE'])
@auth.login_required
def delete_pizza(pizza_id):
    result = pizza_controller.delete_pizza(pizza_id)
    return jsonify(result), 200 if "error" not in result else 400
