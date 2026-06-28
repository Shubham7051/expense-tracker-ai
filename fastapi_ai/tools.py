import requests
from datetime import date


DJANGO_API_URL = "http://127.0.0.1:8000/api/expenses/"
SUMMARY_URL = "http://127.0.0.1:8000/api/expenses/summary/"


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def get_expenses(token):
    response = requests.get(
        DJANGO_API_URL,
        headers=get_headers(token)
    )
    return response.json()


def get_category_summary(token):
    response = requests.get(
        SUMMARY_URL,
        headers=get_headers(token)
    )
    return response.json()


def get_food_expenses(token):
    expenses = get_expenses(token)

    total_food = 0

    for expense in expenses:
        category = expense.get('category', '').lower()
        amount = expense.get('amount', 0)

        if category == 'food':
            total_food += float(amount)

    return round(total_food, 2)


def get_total_expenses(token):
    expenses = get_expenses(token)

    total = 0

    for expense in expenses:
        total += float(expense.get('amount', 0))

    return round(total, 2)


def get_monthly_summary(token):
    expenses = get_expenses(token)

    current_month = date.today().month
    total = 0

    for expense in expenses:
        expense_date = expense.get('date')
        expense_month = int(expense_date.split('-')[1])

        if expense_month == current_month:
            total += float(expense.get('amount', 0))

    return round(total, 2)


def add_expense(token, amount, category, description):
    payload = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(date.today())
    }

    response = requests.post(
        DJANGO_API_URL,
        json=payload,
        headers=get_headers(token)
    )

    return response.json()


def get_financial_context(token):
    return {
        "summary": get_category_summary(token),
        "recent_expenses": get_expenses(token)[:10]
    }


def get_savings_plan_context(token):
    total_expenses = get_total_expenses(token)
    category_summary = get_category_summary(token)
    recent_expenses = get_expenses(token)[:10]
    monthly_summary = get_monthly_summary(token)

    return {
        "total_expenses": total_expenses,
        "category_summary": category_summary,
        "recent_expenses": recent_expenses,
        "monthly_summary": monthly_summary
    }