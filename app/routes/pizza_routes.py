from flask import Blueprint, request, jsonify
from models.db import db
from models.pizza import Pizza
from models.pizza_topping import PizzaTopping
from models.topping import Topping
from models.db import db
from services.topping_service import ToppingService
from controllers.topping_controller import ToppingController

from services.pizza_service import PizzaService
from controllers.pizza_controller import PizzaController

pizza_service = PizzaService(db)
pizza_controller = PizzaController(pizza_service)

pizzas_blueprint = Blueprint('pizzas', __name__, url_prefix='/pizzas')

# Create (POST)
@pizzas_blueprint.route('/', methods=['POST'])
def add_pizza():
    result = pizza_controller.add_pizza()
    return jsonify(result), 201 if "error" not in result else 400

# Read (GET)
@pizzas_blueprint.route('/', methods=['GET'])
def get_pizzas():
    result = pizza_controller.get_pizzas()
    return jsonify(result), 200 if "error" not in result else 400

# Read (GET by ID)
@pizzas_blueprint.route('/<string:pizza_id>', methods=['GET'])
def get_pizza(pizza_id):
    result = pizza_controller.get_pizza(pizza_id)
    return jsonify(result), 200 if "error" not in result else 400

# Update (PUT)
@pizzas_blueprint.route('/<string:pizza_id>', methods=['PUT'])
def update_pizza(pizza_id):
    result = pizza_controller.update_pizza(pizza_id)
    return jsonify(result), 200 if "error" not in result else 400

# Delete (DELETE)
@pizzas_blueprint.route('/<string:pizza_id>', methods=['DELETE'])
def delete_pizza(pizza_id):
    result = pizza_controller.delete_pizza(pizza_id)
    return jsonify(result), 200 if "error" not in result else 400
