import requests
from datetime import date


DJANGO_API_URL = "http://127.0.0.1:8000/api/expenses/"


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNzYyMjA4LCJpYXQiOjE3ODA2NzU4MDgsImp0aSI6Ijk5YjM5NjgwYmE2MzQyMjI5OWYwYWQwYjY0OTZhNjE3IiwidXNlcl9pZCI6IjQifQ.vkILI8k3bDeHVwAb6r_lJcMXwJueddhSKNYT8f06mt0"


headers = {
    "Authorization": f"Bearer {TOKEN}"
}


def get_expenses():

    response = requests.get(
        DJANGO_API_URL,
        headers=headers
    )

    return response.json()


def get_food_expenses() -> float:
    """
    Returns total food expenses.
    """

    expenses = get_expenses()

    total_food = 0

    for expense in expenses:

        category = expense.get(
            'category',
            ''
        ).lower()

        amount = expense.get(
            'amount',
            0
        )

        if category == 'food':

            total_food += float(amount)

    return round(total_food, 2)


def get_total_expenses()->float:
    """
    Returns total expenses.
    """

    expenses = get_expenses()

    total = 0

    for expense in expenses:

        total += float(
            expense.get('amount', 0)
        )

    return round(total, 2)


def get_monthly_summary():
    """
    Returns the monthly summary of the expense.
    """

    expenses = get_expenses()

    current_month = date.today().month

    total = 0

    for expense in expenses:

        expense_date = expense.get('date')

        expense_month = int(
            expense_date.split('-')[1]
        )

        if expense_month == current_month:

            total += float(
                expense.get('amount', 0)
            )

    return round(total, 2)


def add_expense(
    amount: float,
    category: str,
    description: str
):
    """
    Adds a new expense.
    """

    payload = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": "2026-06-05"
    }

    response = requests.post(
        DJANGO_API_URL,
        json=payload,
        headers=headers
    )

    return response.json()