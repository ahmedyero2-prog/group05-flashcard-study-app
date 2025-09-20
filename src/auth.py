import json
import os

# Define the file path for user accounts
USER_DATA_FILE = "C:/Users/okafo/Documents/Python class/Python advanced/group05-flashcard-study-app/data/users.json"

def ensure_user_storage():
    """Ensures the data directory and user file exist."""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({}, f)

def load_users():
    """Loads user accounts from a JSON file."""
    ensure_user_storage()
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Saves user accounts to a JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def login_user(users, username, password):
    """Authenticates a user based on username and password."""
    user = users.get(username)
    if user and user.get("password") == password:
        # Reset session scores on login
        user['session_scores'] = {}
        print("Login successful.")
        return user
    return None

def register_user(users, username, password):
    """Registers a new user account."""
    if username in users:
        print("Username already exists.")
        return None
    
    # Initialize a new user profile with empty data
    new_user = {
        "username": username,
        "password": password,
        "decks": {}
    }
    users[username] = new_user
    save_users(users)
    print("Registration successful.")
    return new_user
