import pytest
from flask import Flask
from app.controllers.topping_controller import ToppingController
from unittest.mock import MagicMock

@pytest.fixture
def app():
    app = Flask(__name__)
    # You might want to configure your app as needed
    return app

@pytest.fixture
def topping_service_mock():
    return MagicMock()

@pytest.fixture
def topping_controller(topping_service_mock, app):
    return ToppingController(topping_service_mock)

def test_add_topping_valid(topping_controller, topping_service_mock, app):
    """Test adding a topping with a valid name."""
    topping_service_mock.add_topping.return_value = {"message": "Topping added successfully"}

    # Mock the request data and use the Flask test client to simulate the request
    with app.test_request_context(json={"topping_name": "Mushroom"}):
        response = topping_controller.add_topping()

    assert response == {"message": "Topping added successfully"}

def test_add_topping_invalid_name_empty(topping_controller, app):
    """Test adding a topping with an empty name."""
    with app.test_request_context(json={"topping_name": ""}):
        response = topping_controller.add_topping()

    assert response == {"error": "Topping name is required."}

def test_add_topping_invalid_name_special_chars(topping_controller, app):
    """Test adding a topping with invalid characters (non-alphabetic)."""
    with app.test_request_context(json={"topping_name": "Mushroom@123"}):
        response = topping_controller.add_topping()

    assert response == {"error": "Topping name must contain only alphabetic characters."}

def test_add_topping_invalid_name_length(topping_controller, app):
    """Test adding a topping with a name that is too long."""
    long_name = "A" * 101
    with app.test_request_context(json={"topping_name": long_name}):
        response = topping_controller.add_topping()

    assert response == {"error": "Topping name must be 1 - 100 characters long."}

def test_update_topping_valid(topping_controller, topping_service_mock, app):
    """Test updating a topping with a valid name."""
    topping_service_mock.update_topping.return_value = {"message": "Topping updated successfully"}

    # Mock the request data and use the Flask test client to simulate the request
    with app.test_request_context(json={"new_topping_name": "Updated Mushroom"}):
        response = topping_controller.update_topping("1")

    assert response == {"message": "Topping updated successfully"}

def test_update_topping_invalid_name_empty(topping_controller, app):
    """Test updating a topping with an empty new name."""
    with app.test_request_context(json={"new_topping_name": ""}):
        response = topping_controller.update_topping("1")

    assert response == {"error": "New topping name is required."}

def test_update_topping_invalid_name_special_chars(topping_controller, app):
    """Test updating a topping with an invalid new name (non-alphabetic)."""
    with app.test_request_context(json={"new_topping_name": "Mushroom@123"}):
        response = topping_controller.update_topping("1")

    assert response == {"error": "New topping name must not contain numbers or special characters."}

def test_update_topping_invalid_name_length(topping_controller, app):
    """Test updating a topping with a new name that is too long."""
    long_name = "A" * 101
    with app.test_request_context(json={"new_topping_name": long_name}):
        response = topping_controller.update_topping("1")

    assert response == {"error": "New topping name must be 1 - 100 characters long."}

def test_delete_topping_valid(topping_controller, topping_service_mock, app):
    """Test deleting a topping with a valid ID."""
    topping_service_mock.delete_topping.return_value = {"message": "Topping deleted successfully"}

    with app.test_request_context():
        response = topping_controller.delete_topping("1")

    assert response == {"message": "Topping deleted successfully"}

def test_delete_topping_invalid_id(topping_controller, app):
    """Test deleting a topping with an invalid ID (empty or non-string)."""
    with app.test_request_context():
        response = topping_controller.delete_topping("")

    assert response == {"error": "Invalid topping ID. It must be a non-empty string."}
