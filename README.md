Simple Password Manager

A command-line password manager built with Python for learning purposes.

Features

- Add, view, search, edit, and delete stored credentials
- Automatically generated record IDs
- Input validation
- Masked password display with an option to reveal passwords
- Password generation using Python's "secrets" module
- Local data persistence using JSON

Requirements

- Python 3 installed

How to Run

Run the main Python script from your terminal:

python password_manager.py

Replace "password_manager.py" with the actual name of the Python file if it is different.

On Windows, you can also use:

py password_manager.py

Data Storage

Credential data is stored locally in a "credentials.json" file alongside the Python script.

This file is excluded from Git and is not included in the GitHub repository.

Security Note

This is an educational project. Credentials are stored in a local JSON file without encryption. It is not intended for storing real passwords or sensitive account information.