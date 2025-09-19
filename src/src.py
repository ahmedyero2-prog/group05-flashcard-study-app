import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import random


# ====================================================================
# BACKEND CLASSES AND FUNCTIONS
# ====================================================================

class Card:
    """Represents a single flashcard."""

    def __init__(self, front: str, back: str):
        self.front = front
        self.back = back

    def to_dict(self):
        return {'front': self.front, 'back': self.back}

    @staticmethod
    def from_dict(card_dict):
        return Card(
            front=card_dict['front'],
            back=card_dict['back']
        )


class Deck:
    """Manages a collection of Card objects."""

    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def to_dict(self):
        return {
            'name': self.name,
            'cards': [card.to_dict() for card in self.cards]
        }

    @classmethod
    def from_dict(cls, deck_dict):
        deck = cls(name=deck_dict['name'])
        deck.cards = [Card.from_dict(card_dict) for card_dict in deck_dict['cards']]
        return deck


def save_deck(deck: Deck):
    """Saves a Deck to a JSON file."""
    if not os.path.exists('data'):
        os.makedirs('data')
    filename = os.path.join('data', f'{deck.name}.json')
    with open(filename, 'w') as f:
        json.dump(deck.to_dict(), f, indent=4)


def load_deck(name: str):
    """Loads a Deck from a JSON file."""
    filename = os.path.join('data', f'{name}.json')
    try:
        with open(filename, 'r') as f:
            deck_dict = json.load(f)
            return Deck.from_dict(deck_dict)
    except FileNotFoundError:
        return None


def get_deck_list():
    """Scans the 'data' directory and returns a list of deck names."""
    if not os.path.exists('data'):
        return []
    deck_files = [f for f in os.listdir('data') if f.endswith('.json')]
    return [os.path.splitext(f)[0] for f in deck_files]


# ====================================================================
# GUI APPLICATION
# ====================================================================

# Global Variables to manage state
current_deck = None
current_card_index = 0
card_flipped = False
root = None

# Color Palette
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
    global root
    root = tk.Tk()
    root.title("Flashcard App")
    root.geometry("600x400")
    root.config(bg=COLORS["background_main"])

    show_deck_selection_page()

    root.mainloop()


def show_deck_selection_page():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(root, text="Flashcard Decks", font=("Helvetica", 20, "bold"), bg=COLORS["background_main"])
    title_label.pack(pady=10)

    deck_buttons_frame = tk.Frame(root, bg=COLORS["background_main"])
    deck_buttons_frame.pack(pady=10)

    deck_names = get_deck_list()
    if not deck_names:
        tk.Label(deck_buttons_frame, text="No decks found. Create one!", bg=COLORS["background_main"]).pack(pady=10)
    else:
        for name in deck_names:
            tk.Button(deck_buttons_frame, text=f"Study {name}", command=lambda n=name: select_deck_and_study(n),
                      bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).pack(pady=5)
            tk.Button(deck_buttons_frame, text=f"Add to {name}", command=lambda n=name: select_deck_and_add(n),
                      bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).pack(pady=5)

    tk.Button(root, text="Create New Deck", command=create_new_deck, bg=COLORS["button_normal"],
              activebackground=COLORS["button_hover"]).pack(pady=10)


def select_deck_and_study(name):
    global current_deck
    current_deck = load_deck(name)
    if current_deck and len(current_deck.cards) > 0:
        random.shuffle(current_deck.cards)
        show_study_page()
    else:
        messagebox.showerror("Error", "Deck not found or has no cards.")


def select_deck_and_add(name):
    global current_deck
    current_deck = load_deck(name)
    if current_deck:
        show_card_creation_page()
    else:
        messagebox.showerror("Error", "Deck not found.")


def create_new_deck():
    new_name = simpledialog.askstring("New Deck", "Enter a name:")
    if new_name:
        if load_deck(new_name):
            messagebox.showerror("Error", "A deck with this name already exists.")
        else:
            new_deck = Deck(name=new_name)
            save_deck(new_deck)
            messagebox.showinfo("Success", f"Deck '{new_name}' created!")
            show_deck_selection_page()


# ====================================================================
# CARD CREATION PAGE
# ====================================================================

front_entry = None
back_entry = None


def show_card_creation_page():
    global front_entry, back_entry
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Add to: {current_deck.name}", font=("Helvetica", 16, "bold"),
             bg=COLORS["background_main"]).pack(pady=10)

    tk.Label(root, text="Front of Card:", bg=COLORS["background_main"]).pack()
    front_entry = tk.Entry(root, width=50)
    front_entry.pack()

    tk.Label(root, text="Back of Card:", bg=COLORS["background_main"]).pack()
    back_entry = tk.Entry(root, width=50)
    back_entry.pack()

    tk.Button(root, text="Save Card", command=save_card, bg=COLORS["button_normal"],
              activebackground=COLORS["button_hover"]).pack(pady=10)
    tk.Button(root, text="Back to Decks", command=show_deck_selection_page, bg=COLORS["button_normal"],
              activebackground=COLORS["button_hover"]).pack()


def save_card():
    front_text = front_entry.get().strip()
    back_text = back_entry.get().strip()

    if front_text and back_text:
        new_card = Card(front=front_text, back=back_text)
        current_deck.add_card(new_card)
        save_deck(current_deck)
        messagebox.showinfo("Success", "Card saved successfully!")
        front_entry.delete(0, tk.END)
        back_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in both fields.")


# ====================================================================
# STUDY PAGE (IMPROVED UI)
# ====================================================================

card_label = None


def show_study_page():
    global card_label, current_card_index, card_flipped
    for widget in root.winfo_children():
        widget.destroy()

    current_card_index = 0
    card_flipped = False

    # Main frame for the study page with a background color
    study_frame = tk.Frame(root, bg="#E6E6FA")
    study_frame.pack(fill="both", expand=True)

    # Use a Frame to create the visual "card" tile
    card_display_frame = tk.Frame(study_frame, bg=COLORS["card_front"], bd=5, relief="raised")
    card_display_frame.pack(pady=20, padx=20, fill="both", expand=True)

    card_label = tk.Label(card_display_frame, text="", font=("Helvetica", 24, "bold"),
                          wraplength=500, bg=COLORS["card_front"], fg=COLORS["text_dark"])
    card_label.pack(pady=40, padx=20, expand=True)

    # Frame for the buttons to use a more structured grid layout
    button_frame = tk.Frame(study_frame, bg="#E6E6FA")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Flip Card", command=flip_card,
              bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).grid(row=0, column=0, padx=10,
                                                                                        pady=5)
    tk.Button(button_frame, text="Next Card", command=next_card,
              bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).grid(row=0, column=1, padx=10,
                                                                                        pady=5)
    tk.Button(button_frame, text="End Session", command=show_deck_selection_page,
              bg=COLORS["button_normal"], activebackground=COLORS["button_hover"]).grid(row=0, column=2, padx=10,
                                                                                        pady=5)

    display_card()


def display_card():
    global card_label, current_card_index, current_deck
    if current_card_index < len(current_deck.cards):
        card = current_deck.cards[current_card_index]
        card_label.config(text=card.front, bg=COLORS["card_front"], fg=COLORS["text_dark"])
    else:
        messagebox.showinfo("Session Complete", "You have finished this study session!")
        show_deck_selection_page()


def flip_card():
    global card_flipped, current_card_index, current_deck
    if current_card_index < len(current_deck.cards):
        card = current_deck.cards[current_card_index]
        if not card_flipped:
            card_label.config(text=card.back, bg=COLORS["card_back"], fg=COLORS["text_dark"])
            card_flipped = True
        else:
            card_label.config(text=card.front, bg=COLORS["card_front"], fg=COLORS["text_dark"])
            card_flipped = False


def next_card():
    global current_card_index, card_flipped
    current_card_index += 1
    card_flipped = False
    display_card()


# Main entry point
if __name__ == "__main__":
    if not load_deck("Science"):
        science_deck = Deck(name="Science")
        science_deck.add_card(Card("What is the capital of France?", "Paris"))
        science_deck.add_card(Card("What is H2O?", "Water"))
        save_deck(science_deck)

    create_main_window()