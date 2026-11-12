from datetime import datetime

def add_expense(expenses):
    print("\n===== ADD EXPENSE =====")
    
    title = input("Enter expense title: ")
    
    amount = float(input("Enter amount: "))
    
    category = input("Enter category: ")
    date = datetime.now().strftime("%Y-%m-%d")
    
    expense = {
        "title": title,
        "amount": amount,
        "category": category,
        "date": date
    }
    
    expenses.append(expense)
    print("Expense added successfully!")
    
def view_expense(expenses):
    print("\n===== ALL EXPENSES =====")
    
    if not expenses:
        print("No expenses found!")
        return
    for index, expense in enumerate(expenses, start=1):
        print(f"\nExpense {index}")
        print("Title:" , expense["title"])
        print("Amount: $", expense["amount"])
        print("Category:", expense["category"])
        print("Date:", expense["date"])
        
def total_expense(expenses):
    total = sum(item["amount"] for item in expenses)
    
    print("\nTotal Expenses: $", total)
