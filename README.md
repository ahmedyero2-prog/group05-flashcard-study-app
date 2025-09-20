🧠 Flashcard Study App – Group 5
📌 Summary
This is a simple, yet robust desktop application for creating, managing, and studying flashcards. Built with Python and Tkinter, it helps users study more effectively through a clean interface and essential features like spaced repetition and progress tracking.

🎯 Learning Objectives
- Object-oriented design: Card, Deck, Session classes
- Special methods and exception handling for malformed decks
- GUI development using Tkinter

✅ Functional Requirements
- Create decks and cards
- Flip cards in study mode
- Record study results
- Persist progress locally

🎨 UI Requirements
- Card view with flip animation (simple fade/replace)
- List of available decks
- Summary of study progress

🚀 MVP Acceptance Criteria
- A user can:
- Create a deck
- Add cards to it
- Run a study session
- Save results locally

🌱 Stretch Goals
- Spaced repetition algorithm
- Import/export decks
- Animated card flip


💻 Technologies Used
- Python 3.10+
- Tkinter – GUI framework
- pipenv – Dependency management
- pytest – Unit testing

🛠️ Getting Started
Prerequisites
- Python 3.10 or higher
- Git
Installation
git clone https://github.com/ahmedyero2-prog/group05-flashcard-study-app.git
cd group05-flashcard-study-app
pipenv install


Running the Application
pipenv run python -m flashcards


A new window should open, and the app will be ready to use.

📂 File Structure
group05-flashcard-study-app/
├── data/                    # Saved flashcard decks in JSON format
├── src/
│   └── flashcards/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── gui.py
│       ├── models.py
│       ├── storage.py
├── tests/
│   └── test_flashcard.py
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md



🧪 Tests
Run all tests using:
pipenv run pytest


At least two tests are located in /tests/test_flashcard.py.

🎥 Demo Video
🔗 Watch the demo


✒️ Credits
- Project Lead: Dalekeee
- Collaboration: ahmedyero2-prog
