from ai.gemini_client import get_gemini_client
from ai.local_explainer import LocalModelUnavailable, explain_locally
from config import settings


def explain_concept(topic: str) -> str:
    provider = settings.explanation_provider.lower()

    if provider in {"local", "auto"} and settings.local_explanation_enabled:
        try:
            return explain_locally(topic)
        except LocalModelUnavailable:
            if provider == "local":
                raise

    prompt = f"""
You are an expert teacher.
Explain the concept below for a learner who may be seeing it for the first time.
Use:
1. A one-sentence definition.
2. A simple explanation.
3. One intuitive example.
4. A short "Remember" takeaway.

Keep it clear and reasonably concise.

Concept:
{topic}
"""
    return get_gemini_client().text(prompt)
