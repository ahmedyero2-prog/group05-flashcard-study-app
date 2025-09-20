import json
import os
from models import Deck, Card
from typing import Dict

DECK_DIR = "C:/Users/okafo/Documents/Python class/Python advanced/group05-flashcard-study-app/data/decks"

def ensure_deck_storage():
    """Ensures the directory for decks exists."""
    os.makedirs(DECK_DIR, exist_ok=True)

def save_deck(deck: Deck):
    """Saves a Deck object to a JSON file."""
    ensure_deck_storage()
    filename = os.path.join(DECK_DIR, f"{deck.name}.json")
    with open(filename, 'w') as f:
        json.dump(deck.to_dict(), f, indent=4)

def load_deck(name: str):
    """Loads a Deck object from a JSON file."""
    filename = os.path.join(DECK_DIR, f"{name}.json")
    try:
        with open(filename, 'r') as f:
            deck_dict = json.load(f)
            return Deck.from_dict(deck_dict)
    except FileNotFoundError:
        return None

def get_all_decks() -> Dict[str, Deck]:
    """Loads all saved decks from the data directory."""
    ensure_deck_storage()
    decks = {}
    for filename in os.listdir(DECK_DIR):
        if filename.endswith('.json'):
            deck_name = filename[:-5]
            deck = load_deck(deck_name)
            if deck:
                decks[deck_name] = deck
    return decks
