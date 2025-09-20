import random
from typing import Dict, List, Any

class Card:
    """Represents a single flashcard with a front and back."""
    def __init__(self, front: str, back: str):
        self.front = front
        self.back = back

    def __repr__(self):
        return f"Card(front='{self.front}', back='{self.back}')"

    def to_dict(self):
        """Converts the Card object to a dictionary for serialization."""
        return {'front': self.front, 'back': self.back}

    @classmethod
    def from_dict(cls, card_dict: Dict[str, str]):
        """Creates a Card object from a dictionary."""
        return cls(card_dict['front'], card_dict['back'])

class Deck:
    """Manages a collection of Card objects and tracks progress."""
    def __init__(self, name: str, cards: List[Card] = None, progress: Dict[str, int] = None):
        self.name = name
        self.cards = cards if cards is not None else []
        self.progress = progress if progress is not None else {'correct': 0, 'total': 0}

    def add_card(self, card: Card):
        """Adds a Card object to the deck."""
        self.cards.append(card)

    def get_shuffled_cards(self):
        """Returns a shuffled list of cards for a quiz session."""
        shuffled_cards = self.cards[:]
        random.shuffle(shuffled_cards)
        return shuffled_cards

    def to_dict(self):
        """Converts the Deck and its Cards to a dictionary."""
        return {
            'name': self.name,
            'cards': [card.to_dict() for card in self.cards],
            'progress': self.progress
        }

    @classmethod
    def from_dict(cls, deck_dict: Dict[str, Any]):
        """Creates a Deck object from a dictionary."""
        cards = [Card.from_dict(card) for card in deck_dict.get('cards', [])]
        progress = deck_dict.get('progress', {'correct': 0, 'total': 0})
        return cls(name=deck_dict['name'], cards=cards, progress=progress)

class Session:
    """Tracks progress for a single study session."""
    def __init__(self, deck_name: str, total_cards: int):
        self.deck_name = deck_name
        self.correct = 0
        self.total = total_cards
