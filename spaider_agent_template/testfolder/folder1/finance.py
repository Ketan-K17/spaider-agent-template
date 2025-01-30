"""
Personal Finance Management System

This script simulates a simple personal finance management system. It takes various
user inputs to calculate a budget, provide a financial summary, and suggest an
investment strategy.

Inputs can be provided as command-line arguments or interactively if not specified.

Positional Arguments:
1. income: The user's total monthly income.
2. rent_mortgage: Monthly rent or mortgage payment
3. utilities: Monthly utilities cost
4. groceries: Monthly groceries expense
5. transportation: Monthly transportation cost
6. insurance: Monthly insurance premiums
7. entertainment: Monthly entertainment budget
8. savings_goal: The amount the user aims to save each month.
9. investment_preference: The user's preferred investment type (stocks/bonds/real estate).
10. has_debt: Whether the user has any debts (yes/no).
11. total_debt: The total amount of debt (0 if has_debt is 'no').

These can also be provided as named arguments with the same names prefixed by '--'.

Example usage:
python script.py 5000 1500 200 400 300 150 200 500 stocks yes 10000
or
python script.py --income 5000 --rent_mortgage 1500 --utilities 200 --groceries 400 
                 --transportation 300 --insurance 150 --entertainment 200 
                 --savings_goal 500 --investment_preference stocks --has_debt yes --total_debt 10000
"""

import argparse

def get_input(prompt, arg_value):
    if arg_value is not None:
        return arg_value
    return input(prompt)

def get_float_input(prompt, arg_value):
    if arg_value is not None:
        return float(arg_value)
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")

def get_expenses(args):
    categories = ["rent_mortgage", "utilities", "groceries", "transportation", "insurance", "entertainment"]
    return {category: getattr(args, category) for category in categories}

def calculate_budget(income, expenses, savings_goal):
    total_expenses = sum(expenses.values())
    remaining = income - total_expenses - savings_goal
    return remaining

def suggest_investment(preference, amount):
    if preference == 'stocks':
        return f"Consider investing ${amount:.2f} in a diversified stock portfolio."
    elif preference == 'bonds':
        return f"Consider investing ${amount:.2f} in government or corporate bonds."
    elif preference == 'real estate':
        return f"Consider investing ${amount:.2f} in real estate investment trusts (REITs)."
    else:
        return f"Consider consulting a financial advisor to invest ${amount:.2f} based on your preference."

def main(args):
    print("Personal Finance Management System")
    
    income = get_float_input("Enter your monthly income: $", args.income)
    expenses = {
        "rent_mortgage": get_float_input("Enter your monthly rent/mortgage: $", args.rent_mortgage),
        "utilities": get_float_input("Enter your monthly utilities cost: $", args.utilities),
        "groceries": get_float_input("Enter your monthly groceries expense: $", args.groceries),
        "transportation": get_float_input("Enter your monthly transportation cost: $", args.transportation),
        "insurance": get_float_input("Enter your monthly insurance premiums: $", args.insurance),
        "entertainment": get_float_input("Enter your monthly entertainment budget: $", args.entertainment)
    }
    savings_goal = get_float_input("Enter your monthly savings goal: $", args.savings_goal)
    investment_preference = get_input("Enter your investment preference (stocks/bonds/real estate): ", args.investment_preference)
    has_debt = get_input("Do you have any debts? (yes/no): ", args.has_debt).lower()
    debt = get_float_input("Enter your total debt amount: $", args.total_debt) if has_debt == 'yes' else 0
    
    budget = calculate_budget(income, expenses, savings_goal)
    
    print("\nFinancial Summary:")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${sum(expenses.values()):.2f}")
    print(f"Savings Goal: ${savings_goal:.2f}")
    print(f"Remaining Budget: ${budget:.2f}")
    print(f"Total Debt: ${debt:.2f}")
    
    if budget > 0:
        print("\nInvestment Suggestion:")
        print(suggest_investment(investment_preference, budget))
    else:
        print("\nWarning: Your expenses and savings goal exceed your income. Consider adjusting your budget.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Personal Finance Management System")
    
    # Remove positional arguments and keep only named arguments
    parser.add_argument("--income", type=float, help="Monthly income")
    parser.add_argument("--rent_mortgage", type=float, help="Monthly rent/mortgage expense")
    parser.add_argument("--utilities", type=float, help="Monthly utilities expense")
    parser.add_argument("--groceries", type=float, help="Monthly groceries expense")
    parser.add_argument("--transportation", type=float, help="Monthly transportation expense")
    parser.add_argument("--insurance", type=float, help="Monthly insurance expense")
    parser.add_argument("--entertainment", type=float, help="Monthly entertainment expense")
    parser.add_argument("--savings_goal", type=float, help="Monthly savings goal")
    parser.add_argument("--investment_preference", choices=["stocks", "bonds", "real estate"], help="Investment preference")
    parser.add_argument("--has_debt", choices=["yes", "no"], help="Whether you have debt")
    parser.add_argument("--total_debt", type=float, help="Total debt amount")

    args = parser.parse_args()
    main(args)