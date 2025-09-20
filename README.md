Flashcard Study App
This is a simple, yet robust, desktop application for creating, managing, and studying flashcards. Built with Python and Tkinter, it is designed to help you study more effectively by providing a clean user interface and essential features for spaced repetition.

✨ Features
Deck Management: Create new decks or load existing ones from the main menu.

Card Creation: Easily add new flashcards to any deck with a dedicated card creation page.

Local Persistence: All decks and cards are automatically saved as local JSON files, so your data is always safe.

Comprehensive Error Handling: The app includes robust, user-friendly pop-up messages for errors from corrupted files or missing dependencies, preventing crashes.

Dynamic Study Mode: Study cards in a randomized order. The app tracks your progress, showing you how many cards you've completed.

Automated Score Tracking: Your score is automatically tracked based on your study habits. Flipping a card to see the answer counts as an incorrect guess, while passing to the next card without flipping counts as a correct one.

Dependency Management: The application will automatically check for and install required dependencies upon first run.

Simple UI: A clean and intuitive user interface designed for a focused study experience.

💻 Technologies Used
Python 3.x

Tkinter: The standard Python library for building graphical user interfaces.

Pillow: A Python Imaging Library used for handling images.

Pytest: A testing framework for writing and running test cases.

🚀 Getting Started
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

🏃 Running Tests
To ensure the application's core logic is working correctly, you can run the test suite using pytest.

Make sure you have navigated to the root directory of the project.

Run the tests using the following command. The --capture=no flag is used to show all print statements, including the confirmation message when tests succeed. The test suite will automatically install pytest if it's not already present.

pytest --capture=no tests/test_models.py


If all tests pass, you will see a All tests passed successfully! message in your terminal.

📂 File Structure
The project follows a clean and logical file structure.

.
├── data/                    # Saved flashcard decks in JSON format
├── src/                     # All application source code
│   ├── main.py              # The main application file
│   ├── models.py            # Data models (Card, Deck, Session)
│   ├── persistence.py       # Handles saving and loading data
│   ├── exceptions.py        # Custom exception classes for robust error handling
│   └── dependencies.py      # Manages the installation of required libraries
├── tests/
│   └── test_core.py       # Pytest files for testing the data models
├── venv/                    # The Python virtual environment
└── .gitignore               # Files and folders to be ignored by Git

📖 Deck Import Guide
The application allows you to create or edit decks externally using a simple JSON format. A detailed guide with an example of the required file structure can be found in the deck_import_guide.txt file in the project's root directory.

You can also access this guide from within the app by navigating to the Help > Deck Import Guide menu.

🤝 Contribution
Feel free to fork the repository and contribute to this project. All suggestions and improvements are welcome!

Fork the repository.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

✒️ Credits
Project Lead: YourGitHubUsername
Collaboration: ahmedyero2-prog,

Special Thanks: To the community for the guidance and resources that made this project possible.