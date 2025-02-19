import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.db import db
from models.topping import Topping
from models.pizza import Pizza
from models.pizza_topping import PizzaTopping
from routes.topping_routes import toppings_blueprint
from routes.pizza_routes import pizzas_blueprint
from auth.auth import auth

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True)

# Configure SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables within the application context
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(toppings_blueprint)
app.register_blueprint(pizzas_blueprint)

# Protect pages with authentication
@app.route('/')
@auth.login_required
def home():
    return render_template('index.html')

@app.route('/owner')
@auth.login_required
def owner():
    return render_template('topping_view.html')

@app.route('/chef')
@auth.login_required
def chef():
    return render_template('pizza_view.html')

if __name__ == "__main__":
    app.run(debug=True)