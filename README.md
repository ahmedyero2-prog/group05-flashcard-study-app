Flashcard Study App
This is a simple, yet robust, desktop application for creating, managing, and studying flashcards. Built with Python and Tkinter, it is designed to help you study more effectively by providing a clean user interface and essential features for spaced repetition and progress tracking.

Project Goals
Learning Objectives
Object-oriented design: Implement Card, Deck, and Session classes with special methods.

Exception handling: Use custom exceptions for robust error handling, especially for malformed decks.

GUI development: Build a user-friendly graphical interface using Tkinter.

Functional Requirements
Create and manage decks and cards.

Flip cards in a study mode.

Record study results and track progress.

Persist data locally by saving and loading progress.

MVP Acceptance Criteria
A user can:

Create a new deck.

Add cards to the deck.

Run a study session.

Save the study results locally.

Stretch Goals
Implement a spaced repetition algorithm.

Add import/export functionality for decks.

Create an animated card flip effect.

Features
Deck Management: Create new decks or load existing ones from the main menu.

Card Creation: Easily add new flashcards to any deck with a dedicated card creation page.

Local Persistence: All decks and cards are automatically saved as local JSON files, so your data is always safe.

Comprehensive Error Handling: The app includes robust, user-friendly pop-up messages for errors from corrupted files or missing dependencies, preventing crashes.

Dynamic Study Mode: Study cards in a randomized order. The app tracks your progress, showing you how many cards you've completed.

Automated Score Tracking: Your score is automatically tracked based on your study habits.

Dependency Management: The application will automatically check for and install required dependencies upon first run.

Simple UI: A clean and intuitive user interface designed for a focused study experience.

Technologies Used
Python 3.x

Tkinter: The standard Python library for building graphical user interfaces.

Pillow: A Python Imaging Library used for handling images.

Pytest: A testing framework for writing and running test cases.

Getting Started
Follow these steps to get the application up and running on your local machine.

Prerequisites
Python 3.7 or higher

Git

Installation
Clone the repository to your local machine using Git.

git clone [https://github.com/ahmedyero2-prog/group05-flashcard-study-app.git](https://github.com/ahmedyero2-prog/group05-flashcard-study-app.git)

Navigate to the project directory.

cd group05-flashcard-study-app

Create a virtual environment to manage project dependencies. This is a best practice to avoid conflicts with your system's Python.

python -m venv venv

Activate the virtual environment.

On Windows:

venv\Scripts\activate

On macOS and Linux:

source venv/bin/activate

Running the Application
With the virtual environment activated, navigate into the source directory.

cd src

Run the main application script. The app will automatically install any missing dependencies for you.

python main.py

A new window should open, and the app will be ready to use.

Running Tests
To ensure the application's core logic is working correctly, you can run the test suite using pytest.

Make sure you have navigated to the root directory of the project.

Run the tests using the following command. The --capture=no flag is used to show all print statements, including the confirmation message when tests succeed.

pytest --capture=no tests/test_core.py

If all tests pass, you will see a All tests passed successfully! message in your terminal.

File Structure
The project follows a clean and logical file structure.

.
├── data/                       # Saved flashcard decks in JSON format
├── src/                        # All application source code
│   ├── exceptions.py           # Custom exception classes for robust error handling
│   ├── main.py                 # The main application file
│   ├── models.py               # Data models (Card, Deck, Session)
│   ├── persistence.py          # Handles saving and loading data
│   ├── __init__.py             # Makes src a Python package
│   └── (and other files like auth.py, etc.)
├── tests/                      # Pytest files for testing the application
│   └── test_core.py            # Test suite for core application logic
├── venv/                       # The Python virtual environment
└── README.md

Deck Import Guide
The application allows you to create or edit decks externally using a simple text format. A detailed guide with an example of the required file structure can be found in the deck_import_guide.txt file in the project's root directory.

You can also access this guide from within the app by navigating to the Help > Deck Import Guide menu.

Credits
Project Lead: 
Collaboration: ahmedyero2-prog, Stevereeds

