import json
import os

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



class Deck:
    """Manages a collection of Card objects."""
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_card(self, card: Card):
        """Adds a Card object to the deck."""
        self.cards.append(card)

    def to_dict(self):
        """Converts the Deck and its Cards to a dictionary."""
        return {
            'name': self.name,
            'cards': [card.to_dict() for card in self.cards]
        }

    @classmethod
    def from_dict(cls, deck_dict):
        """Creates a Deck object from a dictionary."""
        deck = cls(name=deck_dict['name'])
        deck.cards = [Card(card['front'], card['back']) for card in deck_dict['cards']]
        return deck

    def save_deck(deck: Deck):
        """Saves a Deck object to a JSON file."""
        # This line checks if a directory named 'data' exists.
        if not os.path.exists('data'):
            # If the 'data' directory does not exist, this line creates it.
            # This is important to ensure we have a place to save our files.
            os.makedirs('data')
        # os.path.join intelligently combines path components, making the code work on any operating system.
        # It creates the full path to the file, e.g., 'data/Science.json'.
        filename = os.path.join('data', f'{deck.name}.json')
        # The 'with open(...) as f:' block opens the file for writing ('w').
        # It ensures the file is automatically closed, even if errors occur.
        with open(filename, 'w') as f:
            # json.dump() serializes a Python object (the dictionary from deck.to_dict())
            # and writes it to the file. 'indent=4' makes the JSON file human-readable.
            json.dump(deck.to_dict(), f, indent=4)
        print(f"Deck '{deck.name}' saved successfully to '{filename}'.")

    def load_deck(name: str):
        """Loads a Deck object from a JSON file."""
        # This line constructs the expected filename for the deck.
        filename = os.path.join('data', f'{name}.json')
        # The 'try...except' block is for error handling. It's used to gracefully handle
        # the case where the specified deck file does not exist.
        try:
            # This opens the file for reading ('r').
            with open(filename, 'r') as f:
                # json.load() deserializes the JSON data from the file back into a Python dictionary.
                deck_dict = json.load(f)
                # The Deck.from_dict() class method reconstructs the Deck object from the dictionary.
                return Deck.from_dict(deck_dict)
        # If the file is not found, the code inside this 'except' block will be executed.
        except FileNotFoundError:
            print(f"Error: Deck '{name}' not found.")
            return None

    if __name__ == "__main__":
        # This section serves as a test to verify that the save and load functions work correctly.
        # It creates a sample Deck object.
        my_deck = Deck(name="Science")
        # Adds two Card objects to the deck.
        my_deck.add_card(Card("What is the capital of France?", "Paris"))
        my_deck.add_card(Card("What is H2O?", "Water"))

        # Calls the save_deck function to save the created deck.
        save_deck(my_deck)

        # Calls the load_deck function to load the deck we just saved.
        loaded_deck = load_deck("Science")

        # This checks if the loaded_deck is not None (i.e., the load was successful).
        if loaded_deck:
            print("\n--- Loaded Deck Details ---")
            # Prints details of the loaded deck to confirm data integrity.
            print(f"Deck Name: {loaded_deck.name}")
            print(f"Number of cards: {len(loaded_deck.cards)}")
            print("Cards:")
            # Loops through and prints the details of each card in the loaded deck.
            for card in loaded_deck.cards:
                print(f"  - Front: {card.front} | Back: {card.back}")