from ai.gemini_client import get_gemini_client
from config import settings


def answer_question(question: str) -> str:
    if len(question) > settings.max_input_chars:
        raise ValueError(f"Question is too long. Maximum is {settings.max_input_chars} characters.")

    prompt = f"""
You are EduGenie, a helpful educational assistant.
Answer the student's question accurately and concisely.
Explain important reasoning when useful.
If the question is ambiguous, state the assumption you used.
Do not invent citations or claim to have browsed the web.

Student question:
{question}
"""
    return get_gemini_client().text(prompt)
