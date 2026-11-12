def category_report(expenses):
    
    report = {}
    
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        
        report[category] = report.get(category, 0) + amount
        
        print("\n===== CATEGORY REPORT =====")
        
        for category, amount in report .items():
            print(f"{category}: ${amount}")
