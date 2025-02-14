from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.topping import Topping
from models.pizza import Pizza
from models.pizza_topping import PizzaTopping
from routes.topping_routes import toppings_blueprint
from routes.pizza_routes import pizzas_blueprint

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables within the application context
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(toppings_blueprint)
app.register_blueprint(pizzas_blueprint)

# Render pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/owner')
def owner():
    return render_template('owner.html')

if __name__ == "__main__":
    app.run(debug=True)