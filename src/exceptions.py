"""
Custom exception classes for the flashcard study application.

This module defines various exceptions to handle specific error conditions.
"""

class AuthenticationError(Exception):
    def __init__(self, message="Authentication failed. Please check your credentials."):
        self.message = message
        super().__init__(self.message)

class DependencyInstallationError(Exception):
    def __init__(self, package_name, message="Required package is not installed."):
        self.package_name = package_name
        self.message = f"{message}: {package_name}. Please install it using pip."
        super().__init__(self.message)

class DeckLoadError(Exception):
    def __init__(self, deck_name, message="Failed to load the deck."):
        self.deck_name = deck_name
        self.message = f"{message}: {deck_name}. The file may be corrupted or not exist."
        super().__init__(self.message)

class CardError(Exception):
    def __init__(self, message="An error occurred with a card."):
        self.message = message
        super().__init__(self.message)

class DeckError(Exception):
    def __init__(self, message="An error occurred with a deck."):
        self.message = message
        super().__init__(self.message)

class InvalidDeckFileError(DeckLoadError):
    def __init__(self, deck_name, message="The deck file format is invalid or corrupted."):
        super().__init__(deck_name, message)
