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
