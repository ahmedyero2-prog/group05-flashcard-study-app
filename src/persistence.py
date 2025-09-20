import json
import os
from typing import Dict, Any
from models import Deck
from pathlib import Path

# Pathlib version (cleaner & recommended)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DATA_DIR = PROJECT_ROOT / "data"

# Define the base directory for all app data relative to the script's location
#BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "cd.. group05-flashcard-study-app/data")

# Subdirectories for decks and user data
PUBLIC_DECKS_DIR = os.path.join(BASE_DATA_DIR, "decks")
PRIVATE_DECKS_DIR = os.path.join(BASE_DATA_DIR, "decks", "private")
PUBLIC_DECKS_DIR = os.path.join(BASE_DATA_DIR, "decks", "public")
USER_PROGRESS_DIR = os.path.join(BASE_DATA_DIR, "progress")

def ensure_deck_storage():
    """Ensures the necessary deck storage directories exist."""
    os.makedirs(PUBLIC_DECKS_DIR, exist_ok=True)
    os.makedirs(PRIVATE_DECKS_DIR, exist_ok=True)
    os.makedirs(USER_PROGRESS_DIR, exist_ok=True)

def _get_user_deck_path(username: str, deck_id: str) -> str:
    """Returns the file path for a specific user's private deck."""
    user_private_dir = os.path.join(PRIVATE_DECKS_DIR, username)
    os.makedirs(user_private_dir, exist_ok=True)
    return os.path.join(user_private_dir, f"{deck_id}.json")

def _get_public_deck_path(deck_id: str) -> str:
    """Returns the file path for a specific public deck."""
    return os.path.join(PUBLIC_DECKS_DIR, f"{deck_id}.json")
    
def _get_progress_path(username: str, deck_id: str) -> str:
    """Returns the file path for a user's progress on a specific deck."""
    user_progress_dir = os.path.join(USER_PROGRESS_DIR, username)
    os.makedirs(user_progress_dir, exist_ok=True)
    return os.path.join(user_progress_dir, f"{deck_id}.json")

def save_deck_to_private(username: str, deck: Deck):
    """Saves a deck as a private deck for a specific user."""
    ensure_deck_storage()
    deck_path = _get_user_deck_path(username, deck.deck_id)
    with open(deck_path, 'w') as f:
        json.dump(deck.to_dict(), f, indent=4)
    # Also initialize an empty progress file for this new deck
    save_progress(username, deck.deck_id, {"correct": 0, "total": 0})

def save_deck_to_public(deck: Deck):
    """Saves a deck as a public deck."""
    ensure_deck_storage()
    deck_path = _get_public_deck_path(deck.deck_id)
    with open(deck_path, 'w') as f:
        json.dump(deck.to_dict(), f, indent=4)

def load_deck(file_path: str) -> Deck:
    """Loads a deck from a specified file path."""
    with open(file_path, 'r') as f:
        deck_data = json.load(f)
        return Deck.from_dict(deck_data)

def load_all_user_decks(user: Dict[str, Any]) -> Dict[str, Deck]:
    """Loads all decks owned by a specific user, including their progress."""
    decks = {}
    user_private_dir = os.path.join(PRIVATE_DECKS_DIR, user['username'])
    
    if os.path.exists(user_private_dir):
        for filename in os.listdir(user_private_dir):
            if filename.endswith('.json'):
                deck_id = filename.replace('.json', '')
                try:
                    deck_path = os.path.join(user_private_dir, filename)
                    deck = load_deck(deck_path)
                    deck.progress = load_progress(user['username'], deck_id)
                    decks[deck_id] = deck
                except Exception as e:
                    print(f"Error loading deck {filename}: {e}")
    return decks

def load_all_public_decks() -> Dict[str, Deck]:
    """Loads all public decks."""
    decks = {}
    if os.path.exists(PUBLIC_DECKS_DIR):
        for filename in os.listdir(PUBLIC_DECKS_DIR):
            if filename.endswith('.json'):
                deck_id = filename.replace('.json', '')
                try:
                    deck_path = os.path.join(PUBLIC_DECKS_DIR, filename)
                    deck = load_deck(deck_path)
                    decks[deck_id] = deck
                except Exception as e:
                    print(f"Error loading public deck {filename}: {e}")
    return decks

def import_public_deck(username: str, deck: Deck):
    """Imports a public deck by saving a copy to the user's private storage."""
    save_deck_to_private(username, deck)
    print(f"Public deck '{deck.name}' imported for user '{username}'.")
    
def load_progress(username: str, deck_id: str) -> Dict[str, float]:
    """Loads the progress for a user on a specific deck."""
    progress_path = _get_progress_path(username, deck_id)
    if os.path.exists(progress_path):
        with open(progress_path, 'r') as f:
            return json.load(f)
    return {"correct": 0.0, "total": 0.0}

def save_progress(username: str, deck_id: str, progress: Dict[str, float]):
    """Saves the progress for a user on a specific deck."""
    progress_path = _get_progress_path(username, deck_id)
    with open(progress_path, 'w') as f:
        json.dump(progress, f, indent=4)
