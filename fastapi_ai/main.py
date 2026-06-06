from fastapi import FastAPI
from pydantic import BaseModel

import google.generativeai as genai

from dotenv import load_dotenv

import os

from tools import (
    get_food_expenses,
    get_total_expenses,
    get_monthly_summary,
    add_expense
)


load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


app = FastAPI()


class ChatRequest(BaseModel):

    message: str


# ---------------- TOOLS ---------------- #

tools = [
    get_food_expenses,
    get_total_expenses,
    get_monthly_summary,
    add_expense
]


@app.get("/")
def home():

    return {
        "message": "Native Function Calling Agent Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    chat_session = model.start_chat(
        enable_automatic_function_calling=True
    )

    response = chat_session.send_message(
        request.message,
        tools=tools
    )

    return {
        "response": response.text
    }