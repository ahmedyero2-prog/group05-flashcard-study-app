# Flashcard Study App

This is a simple, yet robust, desktop application for creating, managing, and studying flashcards. Built with Python and Tkinter, it is designed to help you study more effectively by providing a clean user interface and essential features for spaced repetition.

---

Features
* Deck Management: Create new decks or load existing ones from the main menu.

* Card Creation: Easily add new flashcards to any deck with a dedicated card creation page.

* Local Persistence: All decks and cards are automatically saved as local JSON files, so your data is always safe.

* Comprehensive Error Handling: The app includes robust error-handling blocks to prevent crashes from corrupted files or permission issues, providing clear, user-friendly pop-up messages instead.

* Dynamic Study Mode: Study cards in a randomized order. The app tracks your progress, showing you how many cards you've completed.

* Automated Score Tracking: Your score is automatically tracked based on your study habits. Flipping a card to see the answer counts as an incorrect guess, while passing to the next card without flipping counts as a correct one.

* Simple UI: A clean and intuitive user interface designed for a focused study experience..

---

## 💻 Technologies Used

* **Python 3.x**
* **Tkinter**: The standard Python library for building graphical user interfaces.

---

## 🚀 Getting Started

Follow these steps to get the application up and running on your local machine.

### Prerequisites

* Python 3.6 or higher
* Git

### Installation

1.  **Clone the repository** to your local machine using Git.

    ```bash
    git clone [https://github.com/ahmedyero2-prog/group05-flashcard-study-app.git](https://github.com/ahmedyero2-prog/group05-flashcard-study-app.git)
    ```

2.  **Navigate** to the project directory.

    ```bash
    cd group05-flashcard-study-app
    ```

3.  **Create a virtual environment** to manage project dependencies. This is a best practice to avoid conflicts with your system's Python.

    ```bash
    python -m venv venv
    ```

4.  **Activate the virtual environment**.

    * On Windows:
        ```bash
        venv\Scripts\activate
        ```
    * On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

### Running the Application

1.  With the virtual environment activated, navigate into the source directory.
    ```bash
    cd src
    ```

2.  Run the main application script.

    ```bash
    python app_final.py
    ```

A new window should open, and the app will be ready to use.

---

## 📂 File Structure

The project follows a clean and logical file structure.

.
├── data/                    # Saved flashcard decks in JSON format
├── src/                     # All application source code
│   └── app_final.py         # The main application file
├── venv/                    # The Python virtual environment
└── .gitignore               # Files and folders to be ignored by Git


---

## 🤝 Contribution

Feel free to fork the repository and contribute to this project. All suggestions and improvements are welcome!

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## ✒️ Credits

* **Project Lead**: [Your GitHub Username]
* **Collaboration**: ahmedyero2-prog,
* **Special Thanks**: To the community for the guidance and resources that made this project possible.
