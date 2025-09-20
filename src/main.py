import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import scrolledtext
import random
import sys
import subprocess
import os
from typing import List, Dict, Any
import re
import uuid

# --- Custom Imports ---
# We use a try-except block here to handle the case where the libraries are not installed.
try:
    from PIL import Image, ImageTk
except ImportError:
    # If Pillow is not installed, we'll handle it below.
    Image, ImageTk = None, None

# Import our custom exception classes
from exceptions import DependencyInstallationError, AuthenticationError, DeckLoadError

# Import our application logic
from auth import login_user, register_user, load_users, get_password_hint
from models import Card, Deck, Session
from persistence import save_deck_to_private, save_deck_to_public, load_all_user_decks, load_all_public_decks, import_public_deck, save_progress

# --- Dependency Check and Installation ---
def check_and_install_dependencies():
    """
    Checks for required dependencies and installs them if they are missing.
    This function must be called before any imports from these libraries.
    """
    try:
        # This will fail with an ImportError if the PIL library is not installed
        from PIL import Image, ImageTk
    except ImportError:
        print("Pillow library not found. Installing now...")
        try:
            # Use the -m option for a robust installation
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("Pillow installed successfully.")
            # Rerun the program to use the newly installed library
            os.execv(sys.executable, ['python'] + sys.argv)
        except subprocess.CalledProcessError as e:
            raise DependencyInstallationError(f"Error installing Pillow: {e}")
        except Exception as e:
            # Catch other potential errors during the installation process
            raise DependencyInstallationError(f"An unexpected error occurred during installation: {e}")

# Call the function before the main app logic runs
check_and_install_dependencies()

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
        self.current_user: Dict[str, Any] = None
        self.current_deck: Deck = None
        self.all_user_decks: Dict[str, Deck] = {}
        self.all_public_decks: Dict[str, Deck] = {}
        self.quiz_session: Session = None
        self.quiz_cards: List[Card] = []
        self.current_card_index = 0
        self.quiz_tries = 1
        self.tries_left = self.quiz_tries
        self.quiz_strictness = 80
        
        # Set a solid background color instead of an image
        self.background_label = tk.Label(self.root, bg=BACKGROUND_COLOR)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.create_main_menu()
        self.create_widgets()
        self.show_login_screen()

    def create_main_menu(self):
        """Creates the main menu bar with File and Help options."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Deck Import Guide", command=self.show_deck_import_guide)
        
    def show_deck_import_guide(self):
        """
        Opens a new window to display the contents of the deck import guide.
        """
        guide_file_path = os.path.join(os.path.dirname(__file__), "..", "deck_import_guide.txt")

        if not os.path.exists(guide_file_path):
            messagebox.showerror("File Not Found", "The deck import guide file could not be found.")
            return

        guide_window = tk.Toplevel(self.root)
        guide_window.title("Deck Import Guide")
        guide_window.geometry("600x400")
        
        text_widget = scrolledtext.ScrolledText(guide_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        try:
            with open(guide_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                text_widget.insert(tk.END, content)
            text_widget.configure(state='disabled') # Make the text read-only
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the guide file: {e}")
            
    def create_widgets(self):
        """Initializes the frames for different parts of the app."""
        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()
        self.main_menu_frame = self.create_main_menu_frame()
        self.deck_creation_frame = self.create_deck_creation_frame()
        self.study_mode_frame = self.create_study_mode_frame()
        self.quiz_mode_frame = self.create_quiz_mode_frame()
        self.quiz_settings_frame = self.create_quiz_settings_frame()

    def show_frame(self, frame_to_show):
        """Switches to a new frame."""
        for frame in [self.login_frame, self.register_frame, self.main_menu_frame, self.deck_creation_frame,
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
        
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, onvalue=1, offvalue=0, command=self.toggle_password_visibility, bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL, selectcolor="#2c2c2c").pack(pady=5)
        
        tk.Button(frame, text="Login", command=self.handle_login, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        tk.Button(frame, text="Register", command=self.show_register_screen, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        tk.Button(frame, text="Show Hint", command=self.handle_show_hint, bg="#e2904a", fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)

        self.login_status_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL)
        self.login_status_label.pack(pady=10)
        return frame

    def create_register_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        tk.Label(frame, text="Register", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=(20, 10))
        
        tk.Label(frame, text="New Username:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.new_username_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.new_username_entry.pack(pady=5)
        
        tk.Label(frame, text="New Password:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.new_password_entry = tk.Entry(frame, show="*", bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.new_password_entry.pack(pady=5)
        
        # New "Show Password" checkbox for registration
        self.show_password_var_reg = tk.IntVar()
        tk.Checkbutton(frame, text="Show Password", variable=self.show_password_var_reg, onvalue=1, offvalue=0, command=self.toggle_password_visibility_reg, bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL, selectcolor="#2c2c2c").pack(pady=5)
        
        tk.Label(frame, text="Password Hint:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.hint_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.hint_entry.pack(pady=5)

        tk.Button(frame, text="Submit Registration", command=self.handle_register, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        tk.Button(frame, text="Back to Login", command=self.show_login_screen, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        
        self.register_status_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL)
        self.register_status_label.pack(pady=10)
        return frame

    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            
    def toggle_password_visibility_reg(self):
        if self.show_password_var_reg.get() == 1:
            self.new_password_entry.config(show="")
        else:
            self.new_password_entry.config(show="*")

    def create_main_menu_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        tk.Label(frame, text="My Decks:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=(20, 10))
        
        # Deck list and scrollbar
        self.deck_list_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        self.deck_list_frame.pack(fill="both", expand=True)

        tk.Button(frame, text="Create New Deck", command=self.show_deck_creation_screen, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=10)
        tk.Button(frame, text="Import Public Deck", command=self.show_public_decks_dialog, bg="#e2904a", fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        tk.Button(frame, text="Logout", command=self.handle_logout, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=5)
        
        self.import_status_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL)
        self.import_status_label.pack(pady=10)
        
        return frame

    def create_deck_creation_frame(self):
        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, bd=5, relief="groove")
        
        tk.Label(frame, text="Create New Deck", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD).pack(pady=(20, 10))
        
        tk.Label(frame, text="Deck Name:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.new_deck_name_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.new_deck_name_entry.pack(pady=5)
        
        # Public/Private Option
        tk.Label(frame, text="Deck Visibility:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.deck_visibility_var = tk.StringVar(value="private")
        radio_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        radio_frame.pack()
        tk.Radiobutton(radio_frame, text="Private", variable=self.deck_visibility_var, value="private", bg=BACKGROUND_COLOR, fg="#F5F5F5", selectcolor="#2c2c2c", font=FONT_NORMAL).pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text="Public", variable=self.deck_visibility_var, value="public", bg=BACKGROUND_COLOR, fg="#F5F5F5", selectcolor="#2c2c2c", font=FONT_NORMAL).pack(side="left", padx=10)

        card_inputs_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        card_inputs_frame.pack(pady=10)
        
        tk.Label(card_inputs_frame, text="Question:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.card_front_entry = tk.Entry(card_inputs_frame, width=40, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.card_front_entry.pack(pady=5)

        tk.Label(card_inputs_frame, text="Answer:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.card_back_entry = tk.Entry(card_inputs_frame, width=40, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.card_back_entry.pack(pady=5)
        
        tk.Label(card_inputs_frame, text="Hint (Optional):", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=5)
        self.card_hint_entry = tk.Entry(card_inputs_frame, width=40, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL)
        self.card_hint_entry.pack(pady=5)

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
        
        self.hint_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL)
        self.hint_label.pack(pady=(0, 10))

        tk.Label(frame, text="Your Answer:", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(pady=(10, 5))
        self.answer_entry = tk.Entry(frame, bg="#2c2c2c", fg="#F5F5F5", insertbackground="#F5F5F5", font=FONT_NORMAL, width=40)
        self.answer_entry.pack(pady=5)

        self.quiz_status_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, fg="#F5F5F5", font=FONT_BOLD)
        self.quiz_status_label.pack(pady=10)

        button_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Check Answer", command=self.check_answer, bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Show Hint", command=self.show_hint, bg="#e2904a", fg="#F5F5F5", font=FONT_BOLD, width=15).pack(side="left", padx=10)
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
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            user = login_user(self.users, username, password)
            self.current_user = user
            self.show_main_menu()
        except AuthenticationError as e:
            self.login_status_label.config(text=str(e), fg=WRONG_COLOR)

    def show_register_screen(self):
        self.show_frame(self.register_frame)
        self.new_username_entry.delete(0, tk.END)
        self.new_password_entry.delete(0, tk.END)
        self.hint_entry.delete(0, tk.END)
        self.register_status_label.config(text="")
        # Reset the "Show Password" checkbox on the registration page
        self.show_password_var_reg.set(0)
        self.new_password_entry.config(show="*")

    def handle_register(self):
        try:
            username = self.new_username_entry.get()
            password = self.new_password_entry.get()
            hint = self.hint_entry.get()
            user = register_user(self.users, username, password, hint)
            self.current_user = user
            self.show_main_menu()
        except AuthenticationError as e:
            self.register_status_label.config(text=str(e), fg=WRONG_COLOR)

    def handle_show_hint(self):
        username = self.username_entry.get()
        hint = get_password_hint(self.users, username)
        messagebox.showinfo("Password Hint", hint)

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
        self.import_status_label.config(text="")

    def update_deck_list(self):
        """Refreshes the list of available decks with their progress."""
        for widget in self.deck_list_frame.winfo_children():
            widget.destroy()

        self.all_user_decks = load_all_user_decks(self.current_user)
        
        if not self.all_user_decks:
            tk.Label(self.deck_list_frame, text="No private decks. Create a new one!", bg=BACKGROUND_COLOR, fg="#F5F5F5").pack(pady=10)

        for deck_id, deck in self.all_user_decks.items():
            progress_total = deck.progress['total']
            if progress_total > 0:
                progress_percent = (deck.progress['correct'] / progress_total) * 100
            else:
                progress_percent = 0
            
            progress_text = f"{progress_percent:.0f}% Learned"
            
            deck_frame = tk.Frame(self.deck_list_frame, bg="#CCCCCC", bd=2, relief="groove")
            deck_frame.pack(fill="x", pady=5)
            
            tk.Label(deck_frame, text=f"{deck.name}", bg="#CCCCCC", fg=TEXT_COLOR, font=FONT_BOLD).pack(side="left", padx=10, pady=5)
            tk.Label(deck_frame, text=progress_text, bg="#CCCCCC", fg="#e2904a", font=FONT_NORMAL).pack(side="left", padx=10, pady=5)
            
            tk.Button(deck_frame, text="Study", command=lambda d=deck: self.start_study_mode(d), bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(side="right", padx=5)
            tk.Button(deck_frame, text="Quiz", command=lambda d=deck: self.show_quiz_settings(d), bg=BUTTON_COLOR, fg="#F5F5F5", font=FONT_NORMAL).pack(side="right", padx=5)
            
    def show_deck_creation_screen(self):
        self.show_frame(self.deck_creation_frame)
        self.new_deck_name_entry.delete(0, tk.END)
        self.card_front_entry.delete(0, tk.END)
        self.card_back_entry.delete(0, tk.END)
        self.card_hint_entry.delete(0, tk.END)
        self.new_cards = []
        self.deck_creation_status.config(text="Enter your first card and click 'Add Card'.")

    def add_card_to_deck(self):
        front = self.card_front_entry.get().strip()
        back = self.card_back_entry.get().strip()
        hint = self.card_hint_entry.get().strip()
        
        if not front or not back:
            self.deck_creation_status.config(text="Question and answer cannot be empty.", fg=WRONG_COLOR)
            return

        self.new_cards.append(Card(front, back, hint))
        self.deck_creation_status.config(text=f"Card '{front}' added. Add another or click 'Finish Deck'.", fg=CORRECT_COLOR)
        self.card_front_entry.delete(0, tk.END)
        self.card_back_entry.delete(0, tk.END)
        self.card_hint_entry.delete(0, tk.END)

    def handle_save_deck(self):
        deck_name = self.new_deck_name_entry.get().strip()
        visibility = self.deck_visibility_var.get()
        
        if not deck_name or not self.new_cards:
            self.deck_creation_status.config(text="Deck name and at least one card are required.", fg=WRONG_COLOR)
            return
            
        new_deck = Deck(name=deck_name, deck_id=str(uuid.uuid4()))
        for card in self.new_cards:
            new_deck.add_card(card)

        if visibility == "public":
            save_deck_to_public(new_deck)
            messagebox.showinfo("Success", f"Deck '{new_deck.name}' saved as public.")
        else:
            save_deck_to_private(self.current_user['username'], new_deck)
            messagebox.showinfo("Success", f"Deck '{new_deck.name}' saved as private.")
            
        self.show_main_menu()
        
    def show_public_decks_dialog(self):
        """Displays a dialog for the user to select a public deck to import."""
        self.all_public_decks = load_all_public_decks()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Import Public Deck")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        
        tk.Label(dialog, text="Select a deck to import:", font=FONT_BOLD).pack(pady=10)
        
        listbox = tk.Listbox(dialog, width=50, height=15)
        listbox.pack(pady=10)

        for deck_id, deck in self.all_public_decks.items():
            listbox.insert(tk.END, deck.name)
            
        def import_selected_deck():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a deck to import.")
                return
            
            selected_name = listbox.get(selected_index[0])
            
            # Find the deck ID by name (this is a simple approach,
            # in a real app you'd use a better way to map listbox items to deck IDs)
            selected_deck = next((d for d in self.all_public_decks.values() if d.name == selected_name), None)

            if selected_deck:
                import_public_deck(self.current_user['username'], selected_deck)
                messagebox.showinfo("Success", f"Deck '{selected_deck.name}' imported successfully!")
                self.show_main_menu()
            dialog.destroy()
            
        tk.Button(dialog, text="Import", command=import_selected_deck, bg=BUTTON_COLOR, fg="#F5F5F5").pack(pady=5)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, bg=BUTTON_COLOR, fg="#F5F5F5").pack(pady=5)
    
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
        self.hint_label.config(text="")
        self.tries_left = self.quiz_tries
        
    def show_hint(self):
        card = self.quiz_cards[self.current_card_index]
        if card.hint:
            self.hint_label.config(text=f"Hint: {card.hint}")
        else:
            self.hint_label.config(text="No hint available for this card.")

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
        # Update progress for the current deck
        if self.current_deck:
            self.current_deck.progress['correct'] += self.quiz_session.correct
            self.current_deck.progress['total'] += self.quiz_session.total
            save_progress(self.current_user['username'], self.current_deck.deck_id, self.current_deck.progress)

        # Display session results
        session_percent = (self.quiz_session.correct / self.quiz_session.total) * 100 if self.quiz_session.total > 0 else 0
        message = f"Quiz finished!\nSession Progress: {self.quiz_session.correct}/{self.quiz_session.total} ({session_percent:.0f}%)"
        
        messagebox.showinfo("Quiz Results", message)
        self.show_main_menu()
        
    def animate_flip(self, canvas, item, text, color="#000000", steps=10):
        """Creates a simple fade-like animation for the card flip."""
        current_fill = canvas.itemcget(item, 'fill')
        self.fade_out(canvas, item, current_fill, color, text, steps=steps)

    def fade_out(self, canvas, item, start_color, end_color, next_text, step=10, steps=10):
        if step > 0:
            fade_percent = (step / steps)
            try:
                # Handle color conversion
                rgb_start = self.root.winfo_rgb(start_color)
                r, g, b = (rgb_start[0] // 256, rgb_start[1] // 256, rgb_start[2] // 256)
                
                new_color_code = '#{0:02x}{1:02x}{2:02x}'.format(
                    int(0 * (1 - fade_percent) + r * fade_percent),
                    int(0 * (1 - fade_percent) + g * fade_percent),
                    int(0 * (1 - fade_percent) + b * fade_percent)
                )
                canvas.itemconfig(item, fill=new_color_code)
            except tk.TclError:
                pass  # Ignore invalid color string
            self.root.after(20, self.fade_out, canvas, item, start_color, end_color, next_text, step - 1, steps)
        else:
            self.fade_in(canvas, item, end_color, next_text, steps=steps)
            
    def fade_in(self, canvas, item, end_color, next_text, step=0, steps=10):
        if step < steps:
            fade_percent = (step / steps)
            try:
                rgb_end = self.root.winfo_rgb(end_color)
                r, g, b = (rgb_end[0] // 256, rgb_end[1] // 256, rgb_end[2] // 256)
                
                new_color_code = '#{0:02x}{1:02x}{2:02x}'.format(
                    int(r * fade_percent),
                    int(g * fade_percent),
                    int(b * fade_percent)
                )
                canvas.itemconfig(item, text=next_text, fill=new_color_code)
            except tk.TclError:
                pass
            self.root.after(20, self.fade_in, canvas, item, end_color, next_text, step + 1, steps)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FlashcardApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
