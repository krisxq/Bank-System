# Simple Bank System

A simple command-line bank system built with Python. Lets you create accounts, deposit, withdraw, transfer money, and view transaction history — all from the terminal.

## Features

- Create accounts with an optional PIN
- Deposit and withdraw money
- Transfer money between accounts
- Check account balance
- View transaction history
- Search accounts by name
- Delete an account
- View all accounts
- Saves data automatically so it's still there next time you run the program

## Requirements

- Python 3
- `colorama` library

Install colorama:
```bash
pip install colorama
```

## How to Run

```bash
python main.py
```

Then follow the on-screen menu and enter the number of the option you want.

## Data Storage

Account data is saved to `bank_data.json` in the same folder, and loaded automatically the next time you start the program.

## Note

This is a learning project for practicing Python (OOP, file handling, error handling) and is not meant for real banking use.
