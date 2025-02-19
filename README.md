# strongmind-swe-assignment

## Building the App
1. **Clone the repository:**
   ```sh
   git clone <repository_url>
   cd <repository_name>
   ```
2. **Create a virtual environment at the root of the project:**
   ```sh
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - macOS/Linux:  
     ```sh
     source venv/bin/activate
     ```
   - Windows (PowerShell):  
     ```sh
     venv\Scripts\Activate
     ```
4. **Install dependencies from `requirements.txt`:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Create a `.env` file in the root directory and add these environment variables:**
   ```ini
   ADMIN_USERNAME=user
   ADMIN_PASSWORD=pass123
   DATABASE_URL=sqlite:///pizza_db.sqlite3
   ```

---

## Running the App
1. **Set required environment variables:**
   ```sh
   export PYTHONPATH=./app
   export FLASK_APP=app/app.py
   ```
   *(On Windows PowerShell, use:)*  
   ```powershell
   $env:PYTHONPATH="./app"
   $env:FLASK_APP="app/app.py"
   ```
2. **Run the Flask app:**
   ```sh
   flask run
   ```
3. **Access the app in a browser:**
   - Copy and paste the provided URL from the terminal (e.g., `http://127.0.0.1:5000`).

---

## Testing the App
1. **Ensure the `PYTHONPATH` is set:**
   ```sh
   export PYTHONPATH=./app
   ```
2. **Run tests using `pytest`:**
   ```sh
   pytest tests/
   ```

---

## Frontend Overview
![IMG_0010](https://github.com/user-attachments/assets/4f2df60c-3aa9-4d59-be56-25b6e0f51c9e)

The frontend is a multi-page application with a **landing page** that provides navigation to two sections:  

1. **Owner Page**  
   - Allows the owner to **create, update, delete, and view toppings**.  
   - Any changes to toppings affect all pizzas using those toppings.  

2. **Chef Page**  
   - Enables the chef to **create, update, delete, and view pizzas**.  
   - The chef can add toppings to pizzas, but only from the available selection created by the owner.  
   - If the owner updates toppings, those changes are automatically reflected in all pizzas and the available topping list.  

The system ensures that owners control the available toppings, while chefs can use them to craft pizzas dynamically.

## Backend Overview
![IMG_0012](https://github.com/user-attachments/assets/4df99cc6-5b35-451c-816e-12c06e0bb22b)

The backend is structured in four distinct layers: **API layer**, **Controller layer**, **Service layer**, and **Database layer**.

1. **API Layer**  
   - Responsible for handling and routing incoming HTTP requests to appropriate endpoints.

2. **Controller Layer**  
   - Handles input parsing and validation, ensuring that incoming data meets the necessary format and constraints.
   - Also performs data integrity checks to make sure that no invalid or duplicate data is passed along to the service layer.

3. **Service Layer**  
   - Encapsulates the business logic of the application. It interacts with the database through SQLAlchemy ORM and ensures that data entries (such as toppings and pizzas) are unique and meet the necessary conditions before processing.
   
4. **Database Layer**  
   - Handles the persistent storage of pizzas and toppings, as well as the relationships between them.
   - Ensures data integrity by maintaining a clean, consistent structure in the database.

This layered architecture, combined with the use of the Singleton pattern and dependency injection, promotes **separation of concerns**, **testability**, and **modularity**, making the system easier to maintain and extend.

## Database Overview
![IMG_0013](https://github.com/user-attachments/assets/d20b5d48-3b0f-442f-9633-b3588f759363)

The database schema consists of three primary tables: **toppings**, **pizzas_toppings**, and **pizzas**.

1. **Toppings Table**  
   - Contains a primary key and a `name` column for each topping.

2. **Pizzas Table**  
   - Contains a primary key and a `name` column for each pizza.

3. **Pizzas_Toppings Table**  
   - Serves as a **junction table** to define the many-to-many relationship between pizzas and toppings. 
   - Contains a primary key along with **foreign keys** that link to both the `pizzas` and `toppings` tables, establishing the associations between specific pizzas and their toppings.

This structure ensures that each pizza can have multiple toppings and each topping can be associated with multiple pizzas, maintaining flexibility in managing pizza creations while ensuring data integrity.
