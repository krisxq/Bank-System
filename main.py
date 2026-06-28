import json
import os
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)

DATA_FILE = "bank_data.json"


class Account:
    def __init__(self, name, balance=0, pin="", history=None):
        self.name = name
        self.balance = balance
        self.pin = pin
        self.history = history if history is not None else []

    def add_history(self, text):
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{time_str}] {text}")

    def deposit(self, amount):
        if amount <= 0:
            print(f"{Fore.RED}Deposit amount must be positive!")
            return False
        self.balance += amount
        self.add_history(f"Deposited Rs. {amount}")
        print(f"{Fore.GREEN}Rs. {amount} deposited. New balance: Rs. {self.balance}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print(f"{Fore.RED}Withdrawal amount must be positive!")
            return False
        if amount > self.balance:
            print(f"{Fore.RED}Insufficient funds! Your balance: Rs. {self.balance}")
            return False
        else:
            self.balance -= amount
            self.add_history(f"Withdrew Rs. {amount}")
            print(f"{Fore.GREEN}Rs. {amount} withdrawn. New balance: Rs. {self.balance}")
            return True

    def check_balance(self):
        print(f"{Fore.CYAN}Account Balance: Rs. {self.balance}")
        return self.balance

    def check_pin(self, pin):
        # If no pin was set on the account, skip the check
        if not self.pin:
            return True
        return self.pin == pin

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "pin": self.pin,
            "history": self.history,
        }

    def __str__(self):
        return f"Account: {self.name} | Balance: Rs. {self.balance}"


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, name, initial_balance=0, pin=""):
        if not account_number:
            print(f"{Fore.RED}Account number cannot be empty!")
            return False
        if not name:
            print(f"{Fore.RED}Account holder name cannot be empty!")
            return False
        if account_number in self.accounts:
            print(f"{Fore.RED}Account {account_number} already exists!")
            return False
        if initial_balance < 0:
            print(f"{Fore.RED}Initial balance cannot be negative!")
            return False
        account = Account(name, initial_balance, pin)
        account.add_history(f"Account created with balance Rs. {initial_balance}")
        self.accounts[account_number] = account
        print(f"{Fore.GREEN}Account created for {name} (Account #: {account_number})")
        return True

    def get_account(self, account_number):
        if account_number not in self.accounts:
            print(f"{Fore.RED}Account {account_number} not found!")
            return None
        return self.accounts[account_number]

    def verify_pin(self, account):
        if not account.pin:
            return True
        entered = input("Enter PIN: ").strip()
        if account.check_pin(entered):
            return True
        print(f"{Fore.RED}Incorrect PIN!")
        return False

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.deposit(amount)

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if account and self.verify_pin(account):
            account.withdraw(amount)

    def check_balance(self, account_number):
        account = self.get_account(account_number)
        if account:
            return account.check_balance()

    def transfer(self, from_acc_num, to_acc_num, amount):
        if from_acc_num == to_acc_num:
            print(f"{Fore.RED}Cannot transfer to the same account!")
            return False
        from_acc = self.get_account(from_acc_num)
        if not from_acc:
            return False
        to_acc = self.get_account(to_acc_num)
        if not to_acc:
            return False
        if not self.verify_pin(from_acc):
            return False
        if amount <= 0:
            print(f"{Fore.RED}Transfer amount must be positive!")
            return False
        if amount > from_acc.balance:
            print(f"{Fore.RED}Insufficient funds! Your balance: Rs. {from_acc.balance}")
            return False
        from_acc.balance -= amount
        to_acc.balance += amount
        from_acc.add_history(f"Transferred Rs. {amount} to account {to_acc_num}")
        to_acc.add_history(f"Received Rs. {amount} from account {from_acc_num}")
        print(f"{Fore.GREEN}Rs. {amount} transferred from {from_acc_num} to {to_acc_num}")
        return True

    def delete_account(self, account_number):
        account = self.get_account(account_number)
        if not account:
            return False
        if not self.verify_pin(account):
            return False
        confirm = input(f"Type YES to confirm deleting account {account_number}: ").strip()
        if confirm == "YES":
            del self.accounts[account_number]
            print(f"{Fore.GREEN}Account {account_number} deleted.")
            return True
        print("Deletion cancelled.")
        return False

    def show_history(self, account_number):
        account = self.get_account(account_number)
        if not account:
            return
        if not account.history:
            print("No transaction history found!")
            return
        print(f"\n{Fore.CYAN}Transaction History for {account_number}:")
        print("-" * 50)
        for entry in account.history:
            print(entry)
        print("-" * 50)

    def search_by_name(self, name):
        name = name.lower()
        matches = {num: acc for num, acc in self.accounts.items() if name in acc.name.lower()}
        if not matches:
            print("No matching accounts found!")
            return
        print(f"\n{Fore.CYAN}Matching Accounts:")
        print("-" * 50)
        for acc_num, account in matches.items():
            print(f"{acc_num}: {account}")
        print("-" * 50)

    def list_all_accounts(self):
        if not self.accounts:
            print("No accounts found!")
            return
        print("\nAll Accounts:")
        print("-" * 50)
        for acc_num, account in self.accounts.items():
            print(f"{acc_num}: {account}")
        print("-" * 50)

    def save_to_file(self):
        data = {num: acc.to_dict() for num, acc in self.accounts.items()}
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"{Fore.RED}Could not save data: {e}")

    def load_from_file(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            for num, info in data.items():
                self.accounts[num] = Account(
                    info.get("name", "Unknown"),
                    info.get("balance", 0),
                    info.get("pin", ""),
                    info.get("history", []),
                )
        except (OSError, json.JSONDecodeError) as e:
            print(f"{Fore.RED}Could not load saved data: {e}")


def get_amount(prompt):
    """Ask for a numeric amount, keep asking until a valid number is entered (or blank to cancel)."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            amount = float(raw)
            return amount
        except ValueError:
            print(f"{Fore.RED}Invalid amount! Please enter a number (or leave blank to cancel).")


def get_account_number(prompt):
    acc_num = input(prompt).strip()
    if not acc_num:
        print(f"{Fore.RED}Account number cannot be empty!")
        return None
    return acc_num


def main():
    bank = Bank()
    bank.load_from_file()

    while True:
        print("\n"*3 + "="*29)
        print(f"{Fore.GREEN}WELCOME TO THE BANK SYSTEM 🏦")
        print("="*29)
        print("1. Create Account")
        print("2. Deposit Money (+ve)")
        print("3. Withdraw Money (Take)")
        print("4. Check Balance")
        print("5. View All Accounts")
        print("6. Transfer Money")
        print("7. Transaction History")
        print("8. Search Account by Name")
        print("9. Delete Account")
        print("10. Exit")
        print("="*29)

        try:
            choice = input("Enter your choice (1-10): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nThank you for using our bank service! Goodbye!")
            bank.save_to_file()
            break

        try:
            if choice == "1":
                account_num = get_account_number("Enter account number: ")
                if account_num is None:
                    continue
                name = input("Enter account holder name: ").strip()
                initial = get_amount("Enter initial balance (optional, press Enter for 0): ")
                if initial is None:
                    initial = 0
                pin = input("Set a PIN (optional, press Enter to skip): ").strip()
                bank.create_account(account_num, name, initial, pin)

            elif choice == "2":
                account_num = get_account_number("Enter account number: ")
                if account_num is None:
                    continue
                amount = get_amount("Enter amount to deposit: ")
                if amount is None:
                    print("Deposit cancelled.")
                    continue
                bank.deposit(account_num, amount)

            elif choice == "3":
                account_num = get_account_number("Enter account number: ")
                if account_num is None:
                    continue
                amount = get_amount("Enter amount to withdraw: ")
                if amount is None:
                    print("Withdrawal cancelled.")
                    continue
                bank.withdraw(account_num, amount)

            elif choice == "4":
                account_num = get_account_number("Enter account number: ")
                if account_num is None:
                    continue
                bank.check_balance(account_num)

            elif choice == "5":
                bank.list_all_accounts()

            elif choice == "6":
                from_acc = get_account_number("Enter your account number: ")
                if from_acc is None:
                    continue
                to_acc = get_account_number("Enter recipient account number: ")
                if to_acc is None:
                    continue
                amount = get_amount("Enter amount to transfer: ")
                if amount is None:
                    print("Transfer cancelled.")
                    continue
                bank.transfer(from_acc, to_acc, amount)

            elif choice == "7":
                account_num = get_account_number("Enter account number: ")
                if account_num is None:
                    continue
                bank.show_history(account_num)

            elif choice == "8":
                name = input("Enter name (or part of it) to search: ").strip()
                if not name:
                    print(f"{Fore.RED}Please enter a name to search!")
                    continue
                bank.search_by_name(name)

            elif choice == "9":
                account_num = get_account_number("Enter account number: ")
                if account_num is None:
                    continue
                bank.delete_account(account_num)

            elif choice == "10":
                print("Thank you for using our bank service! Goodbye!")
                bank.save_to_file()
                break

            else:
                print(f"{Fore.RED}Invalid choice! Please enter a number between 1-10.")

        except (EOFError, KeyboardInterrupt):
            print("\nThank you for using our bank service! Goodbye!")
            bank.save_to_file()
            break
        except Exception as e:
            # Catch-all so one unexpected error doesn't crash the whole program
            print(f"{Fore.RED}Something went wrong: {e}")

        # Save after every action so data isn't lost if the program is closed unexpectedly
        bank.save_to_file()


if __name__ == "__main__":
    main()