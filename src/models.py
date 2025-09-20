import uuid
import random
from typing import Dict, List, Any
from exceptions import CardError

class Card:
    """Represents a single flashcard with a front, back, and optional hint."""
    def __init__(self, front: str, back: str, hint: str = None):
        if not front or not back:
            raise CardError("Card must have both a front and a back.")
        self.front = front.strip()
        self.back = back.strip()
        self.hint = hint.strip() if hint else ""

    def to_dict(self) -> Dict[str, str]:
        """Converts the Card object to a dictionary for serialization."""
        return {
            "front": self.front,
            "back": self.back,
            "hint": self.hint
        }
    
    @staticmethod
    def from_dict(card_data: Dict[str, str]):
        """Creates a Card object from a dictionary."""
        return Card(
            front=card_data.get("front"),
            back=card_data.get("back"),
            hint=card_data.get("hint")
        )

class Deck:
    """Represents a collection of flashcards."""
    def __init__(self, name: str, deck_id: str, cards: List[Card] = None, progress: Dict[str, int] = None):
        self.name = name
        self.deck_id = deck_id
        self.cards = cards if cards is not None else []
        self.progress = progress if progress is not None else {"correct": 0, "total": 0}

    def add_card(self, card: Card):
        """Adds a Card object to the deck."""
        self.cards.append(card)

    def get_shuffled_cards(self) -> List[Card]:
        """Returns a shuffled copy of the deck's cards."""
        shuffled_cards = self.cards[:]
        random.shuffle(shuffled_cards)
        return shuffled_cards

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Deck object to a dictionary for serialization."""
        return {
            "name": self.name,
            "deck_id": self.deck_id,
            "cards": [card.to_dict() for card in self.cards],
            "progress": self.progress
        }

    @staticmethod
    def from_dict(deck_data: Dict[str, Any]):
        """Creates a Deck object from a dictionary."""
        return Deck(
            name=deck_data.get("name"),
            deck_id=deck_data.get("deck_id"),
            cards=[Card.from_dict(card) for card in deck_data.get("cards", [])],
            progress=deck_data.get("progress", {"correct": 0, "total": 0})
        )

class Session:
    """Represents a single study or quiz session."""
    def __init__(self, deck_name: str, total_cards: int):
        self.deck_name = deck_name
        self.total = total_cards
        self.correct = 0
