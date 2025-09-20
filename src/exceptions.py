"""
Custom exception classes for the flashcard study application.

This module defines various exceptions to handle specific error conditions
such as authentication failures, dependency issues, problems loading decks,
and issues with cards or decks themselves.
"""

class AuthenticationError(Exception):
    """Exception raised for errors in the authentication process."""
    def __init__(self, message="Authentication failed. Please check your credentials."):
        self.message = message
        super().__init__(self.message)

class DependencyInstallationError(Exception):
    """Exception raised when a required dependency is not installed."""
    def __init__(self, package_name, message="Required package is not installed."):
        self.package_name = package_name
        self.message = f"{message}: {package_name}. Please install it using pip."
        super().__init__(self.message)

class DeckLoadError(Exception):
    """Base exception for errors that occur during the loading of a deck."""
    def __init__(self, deck_name, message="Failed to load the deck."):
        self.deck_name = deck_name
        self.message = f"{message}: {deck_name}. The file may be corrupted or not exist."
        super().__init__(self.message)

class CardError(Exception):
    """Custom exception for errors related to the Card class."""
    def __init__(self, message="An error occurred with a card."):
        self.message = message
        super().__init__(self.message)

class DeckError(Exception):
    """Custom exception for errors related to the Deck class."""
    def __init__(self, message="An error occurred with a deck."):
        self.message = message
        super().__init__(self.message)

class InvalidDeckFileError(DeckLoadError):
    """
    Custom exception for errors related to invalid deck file formats.
    This is a more specific type of DeckLoadError.
    """
    def __init__(self, deck_name, message="The deck file format is invalid or corrupted."):
        super().__init__(deck_name, message)
