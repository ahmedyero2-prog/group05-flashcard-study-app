import json  # Used for saving and loading data in a simple text format.
import os  # Used for interacting with the computer's file system (like creating folders).
import tkinter as tk  # The main library for building the app's windows and buttons.
from tkinter import messagebox, simpledialog  # Special parts of tkinter for pop-up messages.
import random  # Used for shuffling cards so they appear in a random order.


# ====================================================================
# BACKEND CLASSES AND FUNCTIONS
# ====================================================================

class Card:
    # This is a blueprint for a single flashcard.
    def __init__(self, front: str, back: str):
        # This function runs whenever a new card is created.
        self.front = front  # Stores the text for the front of the card.
        self.back = back  # Stores the text for the back of the card.

    def to_dict(self):
        # This converts the card into a simple dictionary.
        return {'front': self.front, 'back': self.back}

    @staticmethod
    def from_dict(card_dict):
        # This takes a dictionary and turns it back into a Card object.
        return Card(
            front=card_dict['front'],
            back=card_dict['back']
        )


class Deck:
    # This manages a collection of Card objects.
    def __init__(self, name: str):
        # This runs when a new deck is created.
        self.name = name  # Stores the name of the deck.
        self.cards = []  # Creates an empty list to hold the cards.

    def add_card(self, card: Card):
        # This function adds a new card to the deck's list.
        self.cards.append(card)

    def to_dict(self):
        # This converts the entire deck into a dictionary for saving.
        return {
            'name': self.name,
            'cards': [card.to_dict() for card in self.cards]  # Converts each card to a dictionary.
        }

    @classmethod
    def from_dict(cls, deck_dict):
        # This takes a dictionary and turns it back into a Deck object.
        deck = cls(name=deck_dict['name'])
        deck.cards = [Card.from_dict(card_dict) for card_dict in deck_dict['cards']]
        return deck


def save_deck(deck: Deck):
    # This function saves a deck to a file with error checking.
    if not os.path.exists('data'):
        # Checks if a 'data' folder exists.
        try:
            os.makedirs('data')  # Tries to create the 'data' folder.
        except OSError as e:
            # If creating the folder fails (e.g., no permission), show an error.
            messagebox.showerror("Error", f"Failed to create the 'data' directory. Check your permissions.")
            return  # Stop the function if an error occurs.

    filename = os.path.join('data', f'{deck.name}.json')  # Creates the full file path.
    try:
        with open(filename, 'w') as f:
            # Opens the file to write to it.
            json.dump(deck.to_dict(), f, indent=4)  # Saves the deck's data to the file.
    except OSError as e:
        # If saving the file fails (e.g., no permission), show an error.
        messagebox.showerror("Error", f"Failed to save the deck '{deck.name}'. Check your file permissions.")


def load_deck(name: str):
    # This function loads a deck from a file with error checking.
    filename = os.path.join('data', f'{name}.json')
    try:
        with open(filename, 'r') as f:
            # Opens the file to read from it.
            deck_dict = json.load(f)  # Loads the data from the file.
            return Deck.from_dict(deck_dict)  # Converts the loaded data into a Deck object.
    except FileNotFoundError:
        # If the file doesn't exist, show an error message.
        messagebox.showerror("Error", f"The deck '{name}' could not be found.")
        return None  # Return nothing.
    except json.decoder.JSONDecodeError:
        # If the file is broken, show an error message.
        messagebox.showerror("Error", f"Failed to load deck '{name}'. The file may be corrupted.")
        return None
    except Exception as e:
        # This is a catch-all for any other unexpected errors.
        messagebox.showerror("Error", f"An unexpected error occurred while loading deck '{name}'.\n\nDetails: {e}")
        return None


def get_deck_list():
    # This function finds all the deck files in the 'data' folder.
    if not os.path.exists('data'):
        return []  # If the folder doesn't exist, there are no decks.
    deck_files = [f for f in os.listdir('data') if f.endswith('.json')]  # Get all files that end with '.json'.
    return [os.path.splitext(f)[0] for f in deck_files]  # Remove the '.json' part from the names.


# ====================================================================
# GUI APPLICATION
# ====================================================================

# Global variables that can be used by all functions.
current_deck = None  # Holds the deck that is currently loaded.
current_card_index = 0  # Tracks which card we are currently viewing.
card_flipped = False  # True if the back of the card is showing.
root = None  # The main window of the app.

# A dictionary to store all the colors used in the app.
COLORS = {
    "background_main": "#F0F8FF",
    "card_front": "#FFFFFF",
    "card_back": "#ADD8E6",
    "text_dark": "#36454F",
    "button_normal": "#90EE90",
    "button_hover": "#3CB371",
    "button_text": "#36454F"
}


def create_main_window():
    # This function sets up and displays the main window.
    global root  # Access the global 'root' variable.
    root = tk.Tk()  # Creates the main window.
    root.title("Flashcard App")  # Sets the title of the window.
    root.geometry("600x400")  # Sets the size of the window.
    root.config(bg=COLORS["background_main"])  # Sets the background color.

    show_deck_selection_page()  # Calls the function to show the first page.

    root.mainloop()  # Starts the app and waits for user actions.


def show_deck_selection_page():
    # This function displays the page with buttons for each deck.
    for widget in root.winfo_children():
        widget.destroy()  # Deletes everything from the current window.

    title_label = tk.Label(root, text="Flashcard Decks", font=("Helvetica", 20, "bold"), bg=COLORS["background_main"])
    title_label.pack(pady=10)  # Creates and places the title label.

    deck_buttons_frame = tk.Frame(root, bg=COLORS["background_main"])
    deck_buttons_frame.pack(pady=10)  # Creates a container for the deck buttons.

    deck_names = get_deck_list()  # Gets a list of all saved decks.
    if not deck_names:
        # If the list is empty, show a message.
        tk.Label(deck_buttons_frame, text="No decks found. Create one!", bg=COLORS["background_main"]).pack(pady=10)
    else:
        # If there are decks, create buttons for each one.
        for name in deck_names:
            tk.Button(deck_buttons_frame, text=f"Study {name}", command=lambda n=name: select_deck_and_study(n),
                      bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).pack(pady=5)
            tk.Button(deck_buttons_frame, text=f"Add to {name}", command=lambda n=name: select_deck_and_add(n),
                      bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).pack(pady=5)

    tk.Button(root, text="Create New Deck", command=create_new_deck, bg=COLORS["button_normal"],
              activebackground=COLORS["button_hover"]).pack(pady=10)  # Button to create a new deck.


def select_deck_and_study(name):
    # This function loads a deck and starts the study session.
    global current_deck
    try:
        current_deck = load_deck(name)  # Tries to load the selected deck.
        if current_deck and len(current_deck.cards) > 0:
            random.shuffle(current_deck.cards)  # Shuffles the cards randomly.
            show_study_page()  # Displays the study page.
        else:
            messagebox.showerror("Error", "This deck is empty. Please add some cards.")  # Shows an error if the deck is empty.
    except Exception as e:
        # Catches any error during the loading process and shows a message.
        messagebox.showerror("Error", f"Failed to load the deck due to an unexpected error.\n\nDetails: {e}")


def select_deck_and_add(name):
    # This function loads a deck and shows the card creation page.
    global current_deck
    current_deck = load_deck(name)  # Tries to load the deck.
    if current_deck:
        show_card_creation_page()  # If successful, show the card creation page.
    else:
        pass  # If not, the load_deck function already showed an error, so we do nothing.


def create_new_deck():
    # This function asks for a new deck name and creates it.
    new_name = simpledialog.askstring("New Deck", "Enter a name:")  # Opens a small window to ask for a name.
    if new_name is None or new_name.strip() == "":
        # Checks if the user clicked cancel or entered nothing.
        messagebox.showerror("Error", "Deck name cannot be empty.")
        return  # Stops the function.

    if load_deck(new_name):
        # Checks if a deck with this name already exists.
        messagebox.showerror("Error", "A deck with this name already exists.")
    else:
        new_deck = Deck(name=new_name)  # Creates a new Deck object.
        save_deck(new_deck)  # Saves the new, empty deck to a file.
        messagebox.showinfo("Success", f"Deck '{new_name}' created!")  # Shows a success message.
        show_deck_selection_page()  # Refreshes the main page.


# ====================================================================
# CARD CREATION PAGE
# ====================================================================

front_entry = None  # A variable to hold the input box for the front of the card.
back_entry = None  # A variable to hold the input box for the back of the card.


def show_card_creation_page():
    # This function creates the page for adding new cards.
    global front_entry, back_entry
    for widget in root.winfo_children():
        widget.destroy()  # Clears the window of all previous content.

    tk.Label(root, text=f"Add to: {current_deck.name}", font=("Helvetica", 16, "bold"),
             bg=COLORS["background_main"]).pack(pady=10)  # A label showing which deck is being used.

    tk.Label(root, text="Front of Card:", bg=COLORS["background_main"]).pack()
    front_entry = tk.Entry(root, width=50)  # Creates the input box for the front of the card.
    front_entry.pack()

    tk.Label(root, text="Back of Card:", bg=COLORS["background_main"]).pack()
    back_entry = tk.Entry(root, width=50)  # Creates the input box for the back of the card.
    back_entry.pack()

    tk.Button(root, text="Save Card", command=save_card, bg=COLORS["button_normal"],
              activebackground=COLORS["button_hover"]).pack(pady=10)  # The button to save the new card.
    tk.Button(root, text="Back to Decks", command=show_deck_selection_page, bg=COLORS["button_normal"],
              activebackground=COLORS["button_hover"]).pack()  # The button to go back to the deck list.


def save_card():
    # This function gets the text from the input boxes and saves a new card.
    front_text = front_entry.get().strip()  # Gets the text from the front input box and removes extra spaces.
    back_text = back_entry.get().strip()  # Gets the text from the back input box.

    if front_text and back_text:
        # Checks if both fields have text.
        new_card = Card(front=front_text, back=back_text)  # Creates a new Card object.
        current_deck.add_card(new_card)  # Adds the new card to the current deck.
        save_deck(current_deck)  # Saves the updated deck to the file.
        messagebox.showinfo("Success", "Card saved successfully!")  # Shows a success message.
        front_entry.delete(0, tk.END)  # Clears the front input box.
        back_entry.delete(0, tk.END)  # Clears the back input box.
    else:
        messagebox.showerror("Error", "Please fill in both fields.")  # Shows an error if a field is empty.


# ====================================================================
# STUDY PAGE (IMPROVED UI WITH PROGRESS AND SCORE TRACKING)
# ====================================================================

card_label = None  # A variable to hold the label that displays the card text.
progress_label = None  # A variable to hold the label that shows progress.
total_cards = 0  # A variable to store the total number of cards in the deck.
correct_guesses = 0  # A variable to store the count of correct guesses.
is_correct = True  # A flag that tracks if the current guess is correct.


def show_study_page():
    # This function creates and displays the study session page.
    global card_label, progress_label, current_card_index, card_flipped, total_cards, correct_guesses, is_correct
    for widget in root.winfo_children():
        widget.destroy()  # Clears the window of all previous content.

    current_card_index = 0  # Resets the card index to the beginning.
    card_flipped = False  # Resets the card flip state.
    total_cards = len(current_deck.cards)  # Gets the total number of cards.
    correct_guesses = 0  # Resets the score for a new session.
    is_correct = True  # Resets the guess flag for the first card.

    study_frame = tk.Frame(root, bg="#E6E6FA")  # A frame for the whole study page.
    study_frame.pack(fill="both", expand=True)

    progress_label = tk.Label(study_frame, text="", font=("Helvetica", 12), bg="#E6E6FA")
    progress_label.pack(pady=(10, 0))  # A label to show the card progress (e.g., 1 of 10).

    card_display_frame = tk.Frame(study_frame, bg=COLORS["card_front"], bd=5, relief="raised")
    card_display_frame.pack(pady=20, padx=20, fill="both", expand=True)  # A frame that looks like a card.

    card_label = tk.Label(card_display_frame, text="", font=("Helvetica", 24, "bold"),
                          wraplength=500, bg=COLORS["card_front"], fg=COLORS["text_dark"])
    card_label.pack(pady=40, padx=20, expand=True)  # The label that shows the card's text.

    button_frame = tk.Frame(study_frame, bg="#E6E6FA")
    button_frame.pack(pady=10)  # A frame to hold the buttons.

    # Creates and places the buttons for the study session.
    tk.Button(button_frame, text="Flip Card", command=flip_card,
              bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).grid(row=0, column=0, padx=10,
                                                                                        pady=5)

    tk.Button(button_frame, text="Next Card", command=next_card,
              bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).grid(row=0, column=1, padx=10,
                                                                                        pady=5)

    # End Session Button
    tk.Button(study_frame, text="End Session", command=show_deck_selection_page,
              bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).pack(pady=10)

    display_card()  # Shows the first card.
    update_progress()  # Updates the progress label to "Card 1 of [Total]".


def update_progress():
    # This function updates the text of the progress label.
    global progress_label, current_card_index, total_cards
    if total_cards > 0:
        progress_label.config(text=f"Card {current_card_index + 1} of {total_cards}")


def display_card():
    # This function shows the current card's front side.
    global card_label, current_card_index, current_deck
    if current_card_index < len(current_deck.cards):
        # Checks if there are more cards to show.
        card = current_deck.cards[current_card_index]
        card_label.config(text=card.front, bg=COLORS["card_front"], fg=COLORS["text_dark"])  # Updates the label with the card's front text.
    else:
        # If there are no more cards, show a completion message.
        messagebox.showinfo("Session Complete",
                            f"You have finished this study session! You got {correct_guesses} out of {total_cards} correct.")
        show_deck_selection_page()  # Goes back to the main page.


def flip_card():
    # This function switches between the front and back of the card.
    global card_flipped, current_card_index, current_deck, is_correct
    if current_card_index < len(current_deck.cards):
        card = current_deck.cards[current_card_index]
        if not card_flipped:
            # If the card is not flipped, show the back side.
            card_label.config(text=card.back, bg=COLORS["card_back"], fg=COLORS["text_dark"])
            card_flipped = True
            is_correct = False  # User flipped the card, so it's a wrong guess.
        else:
            # If the card is already flipped, show the front side again.
            card_label.config(text=card.front, bg=COLORS["card_front"], fg=COLORS["text_dark"])
            card_flipped = False


def next_card():
    # This function moves to the next card in the deck.
    global current_card_index, card_flipped, correct_guesses, is_correct
    if is_correct:
        correct_guesses += 1  # Increments the score if the guess was correct (card wasn't flipped).

    current_card_index += 1  # Increases the card index by 1.
    card_flipped = False  # Resets the flip state for the new card.
    is_correct = True  # Resets the guess flag for the next card to 'correct' by default.
    update_progress()  # Calls the function to update the progress label.
    display_card()  # Shows the next card's front side.


# The main part of the program that runs when you start the file.
if __name__ == "__main__":
    if not load_deck("Science"):
        # Checks if a 'Science' deck already exists.
        science_deck = Deck(name="Science")  # Creates a default deck.
        science_deck.add_card(Card("What is the capital of France?", "Paris"))
        science_deck.add_card(Card("What is H2O?", "Water"))
        save_deck(science_deck)  # Saves the default deck to a file.

    create_main_window()  # Starts the entire application.