import os
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    expected_username = os.getenv('ADMIN_USERNAME')
    expected_password = os.getenv('ADMIN_PASSWORD')

    if not expected_username or not expected_password:
        return False  # Prevents access if env vars are not set

    return username == expected_username and password == expected_password
