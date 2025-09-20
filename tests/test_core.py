import subprocess
import sys
import os

# Try to import pytest. If it fails, install it and then re-import.
try:
    import pytest
except ImportError:
    print("pytest not found. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
        print("pytest installation successful.")
        import pytest  # Re-import after successful installation
    except subprocess.CalledProcessError as e:
        print(f"Failed to install pytest: {e}")
        # Exit or handle gracefully, as we can't run tests without pytest.
        sys.exit(1)

# Add the project's root directory to the Python path
# so we can import modules from the 'src' directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Card, Deck, Session
from src.exceptions import CardError

def test_card_creation_success():
    """Test that a Card can be created with a front and a back."""
    card = Card("Front Test", "Back Test")
    assert card.front == "Front Test"
    assert card.back == "Back Test"
    assert card.hint == ""

def test_card_creation_with_hint():
    """Test that a Card can be created with a hint."""
    card = Card("Front Test", "Back Test", "Hint Test")
    assert card.front == "Front Test"
    assert card.back == "Back Test"
    assert card.hint == "Hint Test"

def test_card_creation_failure_no_front():
    """Test that a CardError is raised when the front is missing."""
    with pytest.raises(CardError):
        Card("", "Back Test")

def test_card_creation_failure_no_back():
    """Test that a CardError is raised when the back is missing."""
    with pytest.raises(CardError):
        Card("Front Test", "")

def test_card_to_dict():
    """Test that the Card object is correctly converted to a dictionary."""
    card = Card("Front Test", "Back Test", "Hint Test")
    expected_dict = {"front": "Front Test", "back": "Back Test", "hint": "Hint Test"}
    assert card.to_dict() == expected_dict

def test_card_from_dict():
    """Test that a Card object can be created from a dictionary."""
    card_dict = {"front": "Front Test", "back": "Back Test", "hint": "Hint Test"}
    card = Card.from_dict(card_dict)
    assert card.front == "Front Test"
    assert card.back == "Back Test"
    assert card.hint == "Hint Test"

def test_deck_creation_success():
    """Test that a Deck can be created with a name and ID."""
    deck = Deck("Test Deck", "deck_123")
    assert deck.name == "Test Deck"
    assert deck.deck_id == "deck_123"
    assert deck.cards == []
    assert deck.progress == {"correct": 0, "total": 0}

def test_deck_add_card():
    """Test that a Card can be added to the Deck."""
    deck = Deck("Test Deck", "deck_123")
    card = Card("A", "B")
    deck.add_card(card)
    assert len(deck.cards) == 1
    assert deck.cards[0].front == "A"

def test_deck_get_shuffled_cards():
    """Test that get_shuffled_cards returns a new, shuffled list."""
    deck = Deck("Test Deck", "deck_123")
    card1 = Card("A", "B")
    card2 = Card("C", "D")
    deck.add_card(card1)
    deck.add_card(card2)
    shuffled_cards = deck.get_shuffled_cards()
    assert len(shuffled_cards) == 2
    # This check ensures it's a new list, not the original one
    assert shuffled_cards is not deck.cards

def test_deck_to_dict():
    """Test that the Deck object is correctly converted to a dictionary."""
    deck = Deck("Test Deck", "deck_123")
    card = Card("A", "B")
    deck.add_card(card)
    expected_dict = {
        "name": "Test Deck",
        "deck_id": "deck_123",
        "cards": [{"front": "A", "back": "B", "hint": ""}],
        "progress": {"correct": 0, "total": 0}
    }
    assert deck.to_dict() == expected_dict

def test_deck_from_dict():
    """Test that a Deck object can be created from a dictionary."""
    deck_dict = {
        "name": "Test Deck",
        "deck_id": "deck_123",
        "cards": [{"front": "A", "back": "B", "hint": "test hint"}],
        "progress": {"correct": 5, "total": 10}
    }
    deck = Deck.from_dict(deck_dict)
    assert deck.name == "Test Deck"
    assert deck.deck_id == "deck_123"
    assert len(deck.cards) == 1
    assert deck.cards[0].front == "A"
    assert deck.cards[0].hint == "test hint"
    assert deck.progress == {"correct": 5, "total": 10}

def test_session_creation():
    """Test that a Session object can be created."""
    session = Session("Test Deck", 5)
    assert session.deck_name == "Test Deck"
    assert session.total == 5
    assert session.correct == 0

def test_dependencies():
    """
    Test that required dependencies are installed.
    
    This test will fail if the 'Pillow' library is not found,
    alerting the user that a dependency is missing.
    """
    try:
        import PIL
        assert True
    except ImportError:
        assert False, "Required dependency 'Pillow' is not installed."
