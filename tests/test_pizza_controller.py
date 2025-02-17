import pytest
from flask import Flask
from app.controllers.pizza_controller import PizzaController
from unittest.mock import MagicMock

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def pizza_service_mock():
    return MagicMock()

@pytest.fixture
def pizza_controller(pizza_service_mock, app):
    return PizzaController(pizza_service_mock)

# Test adding a valid pizza
def test_add_pizza_valid(pizza_controller, pizza_service_mock, app):
    """Test adding a pizza with a valid name."""
    pizza_service_mock.add_pizza.return_value = {"message": "Pizza added successfully"}
    with app.test_request_context(json={"pizza_name": "Margherita", "topping_ids": [1, 2]}):
        response = pizza_controller.add_pizza()
    assert response == {"message": "Pizza added successfully"}

# Test adding a pizza with an invalid name (empty name)
def test_add_pizza_invalid_name(pizza_controller, app):
    """Test adding a pizza with an invalid name (empty name)."""
    with app.test_request_context(json={"pizza_name": "", "topping_ids": [1, 2]}):
        response = pizza_controller.add_pizza()
    assert response == {"error": "Pizza name is required."}

# Test updating a pizza with a valid name
def test_update_pizza_valid(pizza_controller, pizza_service_mock, app):
    """Test updating a pizza with a valid name."""
    pizza_service_mock.update_pizza.return_value = {"message": "Pizza updated successfully"}
    with app.test_request_context(json={
        "pizza_name": "Updated Pizza",
        "add_topping_ids": [3],
        "remove_topping_ids": [1]
    }):
        response = pizza_controller.update_pizza(1)
    assert response == {"message": "Pizza updated successfully"}

# Test updating a pizza with an invalid name
def test_update_pizza_invalid_name(pizza_controller, app):
    """Test updating a pizza with an invalid name."""
    with app.test_request_context(json={"pizza_name": "", "add_topping_ids": [], "remove_topping_ids": []}):
        response = pizza_controller.update_pizza(1)
    assert response == {"error": "Pizza name is required."}

# Test adding a pizza with non-existent topping IDs
def test_add_pizza_invalid_non_existent_topping_ids(pizza_controller, pizza_service_mock, app):
    """Test adding a pizza with non-existent topping IDs."""
    pizza_service_mock.add_pizza.return_value = {"error": "Invalid topping IDs."}
    with app.test_request_context(json={"pizza_name": "BBQ Chicken", "topping_ids": [999, 1000]}):
        response = pizza_controller.add_pizza()
    assert response == {"error": "Invalid topping IDs."}

# Test updating a pizza with invalid topping IDs (e.g., adding a non-existent topping)
def test_update_pizza_invalid_topping_ids(pizza_controller, pizza_service_mock, app):
    """Test updating a pizza with invalid topping IDs."""
    pizza_service_mock.update_pizza.return_value = {"error": "Invalid topping IDs."}
    with app.test_request_context(json={
        "pizza_name": "Updated Pizza",
        "add_topping_ids": [999],
        "remove_topping_ids": []
    }):
        response = pizza_controller.update_pizza(1)
    assert response == {"error": "Invalid topping IDs."}

# Test updating a pizza with an empty list of toppings to remove
def test_update_pizza_empty_remove_toppings(pizza_controller, pizza_service_mock, app):
    """Test updating a pizza with an empty list of toppings to remove."""
    pizza_service_mock.update_pizza.return_value = {"message": "Pizza updated successfully"}
    with app.test_request_context(json={
        "pizza_name": "Updated Pizza",
        "add_topping_ids": [3],
        "remove_topping_ids": []
    }):
        response = pizza_controller.update_pizza(1)
    assert response == {"message": "Pizza updated successfully"}

# Test deleting a pizza with a valid pizza ID
def test_delete_pizza_valid(pizza_controller, pizza_service_mock, app):
    """Test deleting a pizza with a valid pizza ID."""
    pizza_service_mock.delete_pizza.return_value = {"message": "Pizza deleted successfully"}
    with app.test_request_context():
        response = pizza_controller.delete_pizza(1)
    assert response == {"message": "Pizza deleted successfully"}

# Test adding a pizza with special characters in the pizza name
def test_add_pizza_invalid_name_special_chars(pizza_controller, app):
    """Test adding a pizza with special characters in the pizza name."""
    with app.test_request_context(json={"pizza_name": "Pizza@123", "topping_ids": [1, 2]}):
        response = pizza_controller.add_pizza()
    assert response == {"error": "Pizza name must contain only alphabetic characters."}

# Test updating a pizza with mixed case name
def test_update_pizza_valid_mixed_case(pizza_controller, pizza_service_mock, app):
    """Test updating a pizza with a mixed case pizza name."""
    pizza_service_mock.update_pizza.return_value = {"message": "Pizza updated successfully"}
    with app.test_request_context(json={"pizza_name": "Updated VEGGIE Pizza", "add_topping_ids": [3], "remove_topping_ids": []}):
        response = pizza_controller.update_pizza(1)
    assert response == {"message": "Pizza updated successfully"}
