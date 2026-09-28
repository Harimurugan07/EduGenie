from ai.gemini_client import get_gemini_client
from config import settings


def summarize_text(text: str) -> str:
    if len(text) > settings.max_summary_chars:
        raise ValueError(
            f"Text is too long. Maximum is {settings.max_summary_chars} characters."
        )

    prompt = f"""
Summarize the educational passage below for quick revision.
Preserve the main facts, concepts, relationships, and important terminology.
Remove repetition and irrelevant detail.
Use a short heading followed by concise bullet points.

Passage:
{text}
"""
    return get_gemini_client().text(prompt, temperature=0.2)
