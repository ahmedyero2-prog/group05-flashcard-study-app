import tkinter as tk
import random
import sys
import subprocess
import os
from typing import List
import re

# --- Dependency Check and Installation ---
def check_and_install_dependencies():
    """
    Checks for required dependencies and installs them if they are missing.
    This function must be called before any imports from these libraries.
    """
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("Pillow library not found. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("Pillow installed successfully.")
            # Rerun the program to use the newly installed library
            os.execv(sys.executable, ['python'] + sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"Error installing Pillow: {e}")
            print("Please install it manually by running 'pip install Pillow' in your terminal.")
            sys.exit(1)

# Call the function before any PIL imports
check_and_install_dependencies()

# Now it is safe to import Pillow
from PIL import Image, ImageTk

from auth import load_users, save_users, login_user, register_user
from models import Card, Deck, Session
from persistence import save_deck, get_all_decks

# Constants for UI styling
BACKGROUND_COLOR = "#34495E"
BUTTON_COLOR = "#4a90e2"
TEXT_COLOR = "#000000"  # Black text
FONT_BOLD = ("Helvetica", 16, "bold")
FONT_NORMAL = ("Helvetica", 14)
CARD_BACKGROUND = ["#F5F5F5", "#CCCCCC"] # White and Grey
CORRECT_COLOR = "#2ECC71"
WRONG_COLOR = "#E74C3C"

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("800x600")

        # Load resources and data
        self.users = load_users()
        self.current_user = None
        self.current_deck = None
        self.quiz_session = None
        self.quiz_cards: List[Card] = []
        self.current_card_index = 0
        self.quiz_tries = 1
        self.tries_left = self.quiz_tries
        self.quiz_strictness = 80
        
        # Set a solid background color instead of an image
        self.background_label = tk.Label(self.root, bg=BACKGROUND_COLOR)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.create_widgets()
        self.show_login_screen()

    def create_widgets(self):
        """Initializes the frames for different parts of the app."""
        self.login_frame = self.create_login_frame()
        self.main_menu_frame = self.create_main_menu_frame()
        self.deck_creation_frame = self.create_deck_creation_frame()
        self.study_mode_frame = self.create_study_mode_frame()
        self.quiz_mode_frame = self.create_quiz_mode_frame()
        self.quiz_settings_frame = self.create_quiz_settings_frame()

    def show_frame(self, frame_to_show):
        """Switches to a new frame."""
        for frame in [self.login_frame, self.main_menu_frame, self.deck_creation_frame,
                      self.study_mode_frame, self.quiz_mode_frame, self.quiz_settings_frame]:
            frame.grid_forget()
        frame_to_show.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    # --- Frame Creation Methods ---

    def create_login_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        tk.Label(frame, text="Username:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=(20, 5))
        self.username_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.username_entry.pack(pady=5)
        
        tk.Label(frame, text="Password:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=(10, 5))
        self.password_entry = tk.Entry(frame, show="*", bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.password_entry.pack(pady=5)
        
        tk.Button(frame, text="Login", command=self.handle_login, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        tk.Button(frame, text="Register", command=self.handle_register, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        
        self.login_status_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL)
        self.login_status_label.pack(pady=10)
        return frame

    def create_main_menu_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        tk.Label(frame, text="Choose a Deck:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=(20, 10))
        
        # Deck list and scrollbar
        self.deck_list_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        self.deck_list_frame.pack(fill="both", expand=True)

        tk.Button(frame, text="Create New Deck", command=self.show_deck_creation_screen, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        tk.Button(frame, text="Logout", command=self.handle_logout, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        
        return frame

    def create_deck_creation_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        
        tk.Label(frame, text="Create New Deck", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=(20, 10))
        
        tk.Label(frame, text="Deck Name:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.new_deck_name_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.new_deck_name_entry.pack(pady=5)

        card_inputs_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        card_inputs_frame.pack(pady=10)
        
        tk.Label(card_inputs_frame, text="Question:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.card_front_entry = tk.Entry(card_inputs_frame, width=40, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.card_front_entry.pack(pady=5)

        tk.Label(card_inputs_frame, text="Answer:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.card_back_entry = tk.Entry(card_inputs_frame, width=40, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.card_back_entry.pack(pady=5)

        button_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Add Card", command=self.add_card_to_deck, bg="#e2904a", fg="#F5F5F5", font=FONT_BOLD).pack(side="left", padx=5)
        tk.Button(button_frame, text="Finish Deck", command=self.handle_save_deck, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(side="left", padx=5)
        
        tk.Button(frame, text="Back to Menu", command=self.show_main_menu, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)

        self.deck_creation_status = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL)
        self.deck_creation_status.pack(pady=10)
        
        return frame
    
    def create_study_mode_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        
        self.study_card_canvas = tk.Canvas(frame, width=600, height=300, bg="#F5F5F5", highlightthickness=0)
        self.study_card_canvas.pack(pady=20)
        self.study_card_text = self.study_card_canvas.create_text(300, 150, text="", fill=TEXT_COLOR, font=("Helvetica", 24, "bold"), width=580, justify="center")

        button_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Previous", command=self.show_previous_card_study, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Flip Card", command=self.flip_card_study, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Next", command=self.show_next_card_study, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)
        
        tk.Button(frame, text="Exit Study", command=self.show_main_menu, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        
        return frame

    def create_quiz_mode_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        
        self.quiz_card_canvas = tk.Canvas(frame, width=600, height=300, bg="#F5F5F5", highlightthickness=0)
        self.quiz_card_canvas.pack(pady=20)
        self.quiz_card_text = self.quiz_card_canvas.create_text(300, 150, text="", fill=TEXT_COLOR, font=("Helvetica", 24, "bold"), width=580, justify="center")

        tk.Label(frame, text="Your Answer:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=(10, 5))
        self.answer_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL, width=40)
        self.answer_entry.pack(pady=5)

        self.quiz_status_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD)
        self.quiz_status_label.pack(pady=10)

        button_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Check Answer", command=self.check_answer, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Next Card", command=self.show_next_card_quiz, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)

        return frame

    def create_quiz_settings_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        tk.Label(frame, text="Quiz Settings", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=(20, 10))
        
        tk.Label(frame, text="Number of Tries:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.tries_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.tries_entry.insert(0, "1")
        self.tries_entry.pack(pady=5)

        tk.Label(frame, text="Similarity Strictness (0-100):", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.strictness_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.strictness_entry.insert(0, "80")
        self.strictness_entry.pack(pady=5)
        
        tk.Button(frame, text="Start Quiz", command=self.start_quiz, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        tk.Button(frame, text="Back to Menu", command=self.show_main_menu, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        
        return frame

    # --- Core Application Logic ---

    def handle_login(self):
        username = self.username_entry.get().lower()
        password = self.password_entry.get()
        user = login_user(self.users, username, password)
        if user:
            self.current_user = user
            self.show_main_menu()
        else:
            self.login_status_label.config(text="Login failed. Try again.")

    def handle_register(self):
        username = self.username_entry.get().lower()
        password = self.password_entry.get()
        user = register_user(self.users, username, password)
        if user:
            self.current_user = user
            self.show_main_menu()
        else:
            self.login_status_label.config(text="Registration failed.")

    def handle_logout(self):
        self.current_user = None
        self.show_login_screen()

    def show_login_screen(self):
        self.show_frame(self.login_frame)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.login_status_label.config(text="")

    def show_main_menu(self):
        self.show_frame(self.main_menu_frame)
        self.update_deck_list()

    def update_deck_list(self):
        """Refreshes the list of available decks with their progress."""
        for widget in self.deck_list_frame.winfo_children():
            widget.destroy()

        decks = get_all_decks()
        
        for name, deck in decks.items():
            progress_total = deck.progress['total']
            if progress_total > 0:
                progress_percent = (deck.progress['correct'] / progress_total) * 100
            else:
                progress_percent = 0
            
            progress_text = f"{progress_percent:.0f}% Learned"
            
            deck_frame = tk.Frame(self.deck_list_frame, bg="#CCCCCC", bd=2, relief="groove")
            deck_frame.pack(fill="x", pady=5)
            
            tk.Label(deck_frame, text=f"{name}", bg="#CCCCCC", fg=TEXT_COLOR, font=FONT_BOLD).pack(side="left", padx=10, pady=5)
            tk.Label(deck_frame, text=progress_text, bg="#CCCCCC", fg="#e2904a", font=FONT_NORMAL).pack(side="left", padx=10, pady=5)
            
            tk.Button(deck_frame, text="Study", command=lambda d=deck: self.start_study_mode(d), bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(side="right", padx=5)
            tk.Button(deck_frame, text="Quiz", command=lambda d=deck: self.show_quiz_settings(d), bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(side="right", padx=5)

    def show_deck_creation_screen(self):
        self.show_frame(self.deck_creation_frame)
        self.new_deck_name_entry.delete(0, tk.END)
        self.card_front_entry.delete(0, tk.END)
        self.card_back_entry.delete(0, tk.END)
        self.new_cards = []
        self.deck_creation_status.config(text="Enter your first card and click 'Add Card'.")

    def add_card_to_deck(self):
        front = self.card_front_entry.get().strip()
        back = self.card_back_entry.get().strip()
        
        if not front or not back:
            self.deck_creation_status.config(text="Question and answer cannot be empty.", fg=WRONG_COLOR)
            return

        self.new_cards.append(Card(front, back))
        self.deck_creation_status.config(text=f"Card '{front}' added. Add another or click 'Finish Deck'.", fg=CORRECT_COLOR)
        self.card_front_entry.delete(0, tk.END)
        self.card_back_entry.delete(0, tk.END)

    def handle_save_deck(self):
        deck_name = self.new_deck_name_entry.get().strip()
        
        if not deck_name or not self.new_cards:
            self.deck_creation_status.config(text="Deck name and at least one card are required.", fg=WRONG_COLOR)
            return
            
        new_deck = Deck(name=deck_name)
        for card in self.new_cards:
            new_deck.add_card(card)

        save_deck(new_deck)
        self.show_main_menu()

    # --- Study Mode ---

    def start_study_mode(self, deck: Deck):
        self.current_deck = deck
        self.current_card_index = 0
        self.show_frame(self.study_mode_frame)
        self.show_card_study()

    def show_card_study(self):
        if not self.current_deck.cards:
            self.study_card_canvas.itemconfig(self.study_card_text, text="No cards in this deck.")
            return

        card = self.current_deck.cards[self.current_card_index]
        self.study_card_canvas.itemconfig(self.study_card_text, text=card.front)
        self.study_card_canvas.config(bg=random.choice(CARD_BACKGROUND))
        self.is_flipped = False

    def flip_card_study(self):
        self.is_flipped = not self.is_flipped
        card = self.current_deck.cards[self.current_card_index]
        text_to_show = card.back if self.is_flipped else card.front
        self.animate_flip(self.study_card_canvas, self.study_card_text, text_to_show)

    def show_next_card_study(self):
        self.current_card_index = (self.current_card_index + 1) % len(self.current_deck.cards)
        self.show_card_study()
    
    def show_previous_card_study(self):
        self.current_card_index = (self.current_card_index - 1 + len(self.current_deck.cards)) % len(self.current_deck.cards)
        self.show_card_study()

    # --- Quiz Mode ---

    def show_quiz_settings(self, deck: Deck):
        self.current_deck = deck
        self.show_frame(self.quiz_settings_frame)

    def start_quiz(self):
        try:
            self.quiz_tries = int(self.tries_entry.get())
            if self.quiz_tries < 1:
                raise ValueError
        except ValueError:
            self.quiz_tries = 1
            
        try:
            self.quiz_strictness = int(self.strictness_entry.get())
            if not 0 <= self.quiz_strictness <= 100:
                raise ValueError
        except ValueError:
            self.quiz_strictness = 80
            
        if not self.current_deck.cards:
            self.quiz_status_label.config(text="No cards in this deck.", fg=WRONG_COLOR)
            return

        self.quiz_cards = self.current_deck.get_shuffled_cards()
        self.quiz_session = Session(self.current_deck.name, len(self.quiz_cards))
        self.current_card_index = 0
        self.tries_left = self.quiz_tries
        self.show_frame(self.quiz_mode_frame)
        self.show_card_quiz()

    def show_card_quiz(self):
        if self.current_card_index >= len(self.quiz_cards):
            self.end_quiz()
            return
            
        card = self.quiz_cards[self.current_card_index]
        self.quiz_card_canvas.itemconfig(self.quiz_card_text, text=card.front, fill=TEXT_COLOR)
        self.quiz_card_canvas.config(bg=random.choice(CARD_BACKGROUND))
        self.answer_entry.delete(0, tk.END)
        self.quiz_status_label.config(text="")
        self.tries_left = self.quiz_tries

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        correct_answer = self.quiz_cards[self.current_card_index].back.strip()
        
        if self.is_similar(user_answer, correct_answer, self.quiz_strictness):
            self.quiz_session.correct += 1
            self.quiz_status_label.config(text="Correct!", fg=CORRECT_COLOR)
            self.animate_flip(self.quiz_card_canvas, self.quiz_card_text, self.quiz_cards[self.current_card_index].back, color=CORRECT_COLOR)
            self.root.after(1500, self.show_next_card_quiz)
        else:
            self.tries_left -= 1
            if self.tries_left > 0:
                self.quiz_status_label.config(text=f"Incorrect. Tries left: {self.tries_left}", fg=WRONG_COLOR)
            else:
                self.quiz_status_label.config(text="Wrong Answer.", fg=WRONG_COLOR)
                self.animate_flip(self.quiz_card_canvas, self.quiz_card_text, self.quiz_cards[self.current_card_index].back, color=WRONG_COLOR)
                self.root.after(1500, self.show_next_card_quiz)
                
    def is_similar(self, user_answer, correct_answer, strictness):
        """
        Checks if two strings are similar based on a given strictness level.
        For dates, it requires an exact match.
        """
        user_lower = user_answer.strip().lower()
        correct_lower = correct_answer.strip().lower()

        # Check for dates - simple check for now
        if re.search(r'\d{4}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}', user_lower) and user_lower != correct_lower:
            return False

        # Tokenize and clean up strings
        user_words = set(re.findall(r'\b\w+\b', user_lower))
        correct_words = set(re.findall(r'\b\w+\b', correct_lower))
        
        # Remove common stop words for general text comparison
        stop_words = {"the", "a", "an", "is", "of", "in", "to", "for", "on", "and", "by"}
        user_words = user_words - stop_words
        correct_words = correct_words - stop_words

        if not user_words or not correct_words:
            return user_lower == correct_lower

        intersection = user_words.intersection(correct_words)
        union = user_words.union(correct_words)
        
        similarity_score = (len(intersection) / len(union)) * 100
        return similarity_score >= strictness

    def show_next_card_quiz(self):
        self.current_card_index += 1
        self.show_card_quiz()

    def end_quiz(self):
        # Update cumulative progress
        self.current_deck.progress['correct'] += self.quiz_session.correct
        self.current_deck.progress['total'] += self.quiz_session.total
        save_deck(self.current_deck)
        
        # Display session results
        session_percent = (self.quiz_session.correct / self.quiz_session.total) * 100 if self.quiz_session.total > 0 else 0
        message = f"Quiz finished!\nSession Progress: {self.quiz_session.correct}/{self.quiz_session.total} ({session_percent:.0f}%)"
        
        result_window = tk.Toplevel(self.root, bg="#2c2c2c")
        result_window.title("Quiz Results")
        result_window.geometry("400x200")
        tk.Label(result_window, text=message, bg="#2c2c2c", fg="#F5F5F5", font=FONT_BOLD).pack(pady=20)
        tk.Button(result_window, text="OK", command=lambda: [result_window.destroy(), self.show_main_menu()], bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack()
        
    def animate_flip(self, canvas, item, text, color="#000000", steps=10):
        """Creates a simple fade-like animation for the card flip."""
        current_fill = canvas.itemcget(item, 'fill')
        self.fade_out(canvas, item, current_fill, color, text, steps=steps)

    def fade_out(self, canvas, item, start_color, end_color, next_text, step=10, steps=10):
        if step > 0:
            fade_percent = (step / steps)
            new_color_code = '#{0:02x}{1:02x}{2:02x}'.format(
                int(0 * (1 - fade_percent) + self.root.winfo_rgb(start_color)[0]/256 * fade_percent),
                int(0 * (1 - fade_percent) + self.root.winfo_rgb(start_color)[1]/256 * fade_percent),
                int(0 * (1 - fade_percent) + self.root.winfo_rgb(start_color)[2]/256 * fade_percent)
            )
            canvas.itemconfig(item, fill=new_color_code)
            self.root.after(20, self.fade_out, canvas, item, start_color, end_color, next_text, step - 1, steps)
        else:
            self.fade_in(canvas, item, end_color, next_text, steps=steps)
            
    def fade_in(self, canvas, item, end_color, next_text, step=0, steps=10):
        if step < steps:
            fade_percent = (step / steps)
            new_color_code = '#{0:02x}{1:02x}{2:02x}'.format(
                int(self.root.winfo_rgb(end_color)[0]/256 * fade_percent),
                int(self.root.winfo_rgb(end_color)[1]/256 * fade_percent),
                int(self.root.winfo_rgb(end_color)[2]/256 * fade_percent)
            )
            canvas.itemconfig(item, text=next_text, fill=new_color_code)
            self.root.after(20, self.fade_in, canvas, item, end_color, next_text, step + 1, steps)

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
