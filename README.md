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
