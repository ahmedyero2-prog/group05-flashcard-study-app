import json
import os
import hashlib
from typing import Dict, Any

from exceptions import AuthenticationError

# Paths for data storage

from pathlib import Path

# Pathlib version (cleaner & recommended)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def _ensure_dir_exists(path):
    """Helper function to create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def _hash_password(password: str) -> str:
    """Hashes a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> Dict[str, Any]:
    """Loads user data from the users file."""
    _ensure_dir_exists(DATA_DIR)
    if not os.path.exists(USERS_FILE):
        return {}
    
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users: Dict[str, Any]):
    """Saves user data to the users file."""
    _ensure_dir_exists(DATA_DIR)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(users: Dict[str, Any], username: str, password: str, hint: str) -> Dict[str, str]:
    """Registers a new user, saving their details."""
    if not username or not password or not hint:
        raise AuthenticationError("Username, password, and hint cannot be empty.")
    if username in users:
        raise AuthenticationError("Username already exists.")

    hashed_password = _hash_password(password)
    users[username] = {
        "password": hashed_password,
        "hint": hint
    }
    save_users(users)
    return {"username": username}

def login_user(users: Dict[str, Any], username: str, password: str) -> Dict[str, str]:
    """Authenticates a user and returns their data."""
    if username not in users:
        raise AuthenticationError("User not found.")
    
    hashed_password = _hash_password(password)
    if users[username]["password"] != hashed_password:
        raise AuthenticationError("Incorrect password.")

    return {"username": username}

def get_password_hint(users: Dict[str, Any], username: str) -> str:
    """Retrieves the password hint for a given user."""
    if username not in users:
        return "User not found."
    return users[username].get("hint", "No hint available.")
