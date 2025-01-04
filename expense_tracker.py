import json
import os
from colorama import Fore, Style

EXPENSES_FILE = 'expenses.txt'
expenses = []

EXCHANGE_RATES = {
    'USD': 1,
    'EUR': 0.85,
    'GBP': 0.75,
    'INR': 75.0,
    'AUD': 1.35
}

def load_expenses():
        global expenses
        if os.path.exists(EXPENSES_FILE):
            with open(EXPENSES_FILE, 'r') as file:
                try:
                    expenses = json.load(file)
                except json.JSONDecodeError:
                    print(
                        Fore.RED + "Error loading expenses: The file is empty or contains invalid data." + Style.RESET_ALL)
                    expenses = []
        else:

            with open(EXPENSES_FILE, 'w') as file:
                json.dump([], file)
            expenses = []


def save_expenses():
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file)

def add_expense():
    amount = float(input("Enter expense amount in USD: $"))
    category = input("Enter expense category (e.g., Food, Transport, Entertainment): ")
    date = input("Enter expense date (YYYY-MM-DD): ")
    currency = input("Enter the currency for this expense (USD, EUR, GBP, INR, AUD): ").upper()
    if currency in EXCHANGE_RATES:
        converted_amount = amount * EXCHANGE_RATES[currency]
        expense = {"amount": converted_amount, "currency": currency, "category": category, "date": date}
        expenses.append(expense)
        save_expenses()
        print(Fore.GREEN + f"Expense added successfully! Converted amount in {currency}: {converted_amount:.2f}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid currency. Expense not added." + Style.RESET_ALL)

def check_budget_limit(budget):
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        category_totals[category] = category_totals.get(category, 0) + expense['amount']
    for category, total in category_totals.items():
        if category in budget and total > budget[category]:
            print(Fore.RED + f"Alert: You exceeded your budget for {category}! Total spent: {total}, Budget: {budget[category]}" + Style.RESET_ALL)
        else:
            print(f"You're within the budget for {category}. Total spent: {total}, Budget: {budget.get(category, 0)}")

def display_expenses():
    print("\n----- Expense Summary -----")
    if not expenses:
        print(Fore.YELLOW + "No expenses recorded yet." + Style.RESET_ALL)
    else:
        for expense in expenses:
            print(f"{expense['date']} | {expense['category']} | {expense['currency']} {expense['amount']}")

def delete_expense():
    date = input("Enter the date of the expense you want to delete (YYYY-MM-DD): ")
    category = input("Enter the category of the expense you want to delete: ")
    global expenses
    expenses = [expense for expense in expenses if not (expense['date'] == date and expense['category'] == category)]
    save_expenses()
    print(Fore.RED + "Expense deleted successfully!" + Style.RESET_ALL)

def filter_expenses_by_date():
    date = input("Enter the date (YYYY-MM-DD) to filter expenses: ")
    filtered_expenses = [expense for expense in expenses if expense['date'] == date]
    print("\n----- Filtered Expenses -----")
    if not filtered_expenses:
        print(Fore.YELLOW + f"No expenses found for {date}." + Style.RESET_ALL)
    else:
        for expense in filtered_expenses:
            print(f"{expense['date']} | {expense['category']} | {expense['currency']} {expense['amount']}")

def generate_monthly_report():
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")
    filtered_expenses = [expense for expense in expenses if expense['date'].startswith(f"{year}-{month}")]
    print("\n----- Monthly Report -----")
    if not filtered_expenses:
        print(Fore.YELLOW + f"No expenses recorded for {month}/{year}." + Style.RESET_ALL)
    else:
        total_expenses = sum(expense['amount'] for expense in filtered_expenses)
        print(f"Total Expenses for {month}/{year}: {total_expenses:.2f}")
        for expense in filtered_expenses:
            print(f"{expense['date']} | {expense['category']} | {expense['currency']} {expense['amount']}")

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    amount_in_usd = amount / EXCHANGE_RATES[from_currency]
    converted_amount = amount_in_usd * EXCHANGE_RATES[to_currency]
    return converted_amount

def currency_converter():
    amount = float(input("Enter amount to convert: "))
    from_currency = input("Enter the currency of the amount (USD, EUR, GBP, INR, AUD): ").upper()
    to_currency = input("Enter the currency you want to convert to (USD, EUR, GBP, INR, AUD): ").upper()
    if from_currency in EXCHANGE_RATES and to_currency in EXCHANGE_RATES:
        converted_amount = convert_currency(amount, from_currency, to_currency)
        print(Fore.GREEN + f"Converted amount: {converted_amount:.2f} {to_currency}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid currency code entered." + Style.RESET_ALL)

def main():
    budget = {}
    load_expenses()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter Expenses by Date")
        print("4. Delete Expense")
        print("5. Set/Update Budget")
        print("6. View Expenses and Check Budget")
        print("7. Generate Monthly Report")
        print("8. Currency Converter")
        print("9. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            display_expenses()
        elif choice == '3':
            filter_expenses_by_date()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            category = input("Enter category (e.g., Food, Transport, Entertainment): ")
            budget_amount = float(input(f"Enter budget for {category}: $"))
            budget[category] = budget_amount
            print(Fore.GREEN + f"Budget for {category} set to ${budget_amount}." + Style.RESET_ALL)
        elif choice == '6':
            display_expenses()
            check_budget_limit(budget)
        elif choice == '7':
            generate_monthly_report()
        elif choice == '8':
            currency_converter()
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
