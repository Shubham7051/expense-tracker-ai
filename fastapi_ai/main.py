from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import google.generativeai as genai
from dotenv import load_dotenv
import os

from auth import verify_token

from tools import (
    get_food_expenses,
    get_total_expenses,
    get_monthly_summary,
    add_expense,
    get_category_summary,
    get_financial_context,
    get_savings_plan_context
)

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-flash-lite-latest"
)

app = FastAPI()
security = HTTPBearer()


SYSTEM_PROMPT = """
You are an advanced AI financial assistant.

Your job is to:
- analyze expenses
- detect overspending
- create savings plans
- provide actionable advice

Always provide clear and practical responses.
"""


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Native Function Calling Agent Running"
    }


@app.post("/chat")
def chat(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    # ---------------- AUTH ---------------- #

    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    print("Authenticated User:", payload)

    # ---------------- PROMPT ---------------- #

    final_prompt = f"""
    {SYSTEM_PROMPT}

    User Message:
    {request.message}
    """

    # ---------------- WRAPPER TOOLS ---------------- #

    def get_food_expenses_tool():
        """Returns total food expenses."""
        return get_food_expenses(token)

    def get_total_expenses_tool():
        """Returns total expenses."""
        return get_total_expenses(token)

    def get_monthly_summary_tool():
        """Returns monthly expense summary."""
        return get_monthly_summary(token)

    def get_category_summary_tool():
        """Returns category-wise summary."""
        return get_category_summary(token)

    def add_expense_tool(
        amount: float,
        category: str,
        description: str
    ):
        """Adds a new expense."""
        return add_expense(
            token,
            amount,
            category,
            description
        )

    def get_financial_context_tool():
        """Returns complete financial context."""
        return get_financial_context(token)

    def get_savings_plan_context_tool():
        """Returns financial context for savings planning."""
        return get_savings_plan_context(token)

    tools = [
        get_food_expenses_tool,
        get_total_expenses_tool,
        get_monthly_summary_tool,
        get_category_summary_tool,
        add_expense_tool,
        get_financial_context_tool,
        get_savings_plan_context_tool
    ]

    # ---------------- GEMINI ---------------- #

    try:
        chat_session = model.start_chat(
            enable_automatic_function_calling=True
        )

        response = chat_session.send_message(
            final_prompt,
            tools=tools
        )

        return {
            "response": response.text
        }

    except Exception as e:
        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )